<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Log;

use App\Models\VotedElectionsModel;
use App\Models\BlockchainCommunicatorModel;

use Carbon\Carbon;

class BlockchainCommunicationController extends Controller
{
    private $user_info;
    private $cipher;
    private $options;

    public function __construct()
    {
        $this->middleware(function($request, $next)
        {
            $this->user_info = Auth::user();
            return $next($request);
        });
        $this->cipher = 'AES-128-CBC';
        $this->options = OPENSSL_RAW_DATA;
    }

    /**
     * Get transaction
     * 
     * This is a function used in API route
     * 
     * @param Request $request:
     * 
     * @return
     */
    public function getTransaction(Request $request)
    {
        $blockchain_communicator = new BlockchainCommunicatorModel();

        $tx_data = [
            'headers' => [
                'tx_hash' => $request['headers']['tx_hash']
            ],
            'tx_details' => [
                'tx_type' => 'view_tx'
            ]
        ];

        return $blockchain_communicator->sendMessage($tx_data);
    }

    /**
     * Get transaction
     * 
     * This is a function used in web route
     * 
     * @param Request $request:
     * 
     * @return
     */
    public function getLatestTransaction()
    {
        $blockchain_communicator = new BlockchainCommunicatorModel();
        
        $latest_tx = [
            'tx_details' => [
                'tx_type' => 'latest_tx'
            ]
        ];
        $latest_tx = $blockchain_communicator->sendMessage($latest_tx);

        return json_decode($latest_tx);
    }
    
    /**
     * Get transaction
     * 
     * This is a function used in web route
     * 
     * @param Request $request:
     * 
     * @return
     */
    public function listElections($show_voted = False)
    {
        $blockchain_communicator = new BlockchainCommunicatorModel();

        $tx_data = [
            'tx_details' => [
                'tx_type' => 'list_elections'
            ]
        ];
        $tx_data = $blockchain_communicator->sendMessage($tx_data);

        if ($show_voted == False) {
            $voted_elections = new VotedElectionsModel();
            //  TODO: Filter voted elections out of the list
        }

        return json_decode($tx_data);
    }

    /**
     * Get transaction
     * 
     * This is a function used in web route
     * 
     * @param Request $request:
     * 
     * @return
     */
    public function getElection($election_txid)
    {
        $blockchain_communicator = new BlockchainCommunicatorModel();

        $tx_data = [
            'headers' => [
                'tx_hash' => $election_txid
            ],
            'tx_details' => [
                'tx_type' => 'view_tx'
            ]
        ];
        $tx_data = $blockchain_communicator->sendMessage($tx_data);
        $tx_data = json_decode($tx_data);
        $tx_data->valid_election = False;

        if (isset($tx_data->tx_details->specfied_tx_details)) {
            if ($tx_data->tx_details->specified_tx_details->tx_details->tx_type == 'add_election') {
                $tx_data[] = [
                    'valid_election' => True
                ];
            }
        }

        return $tx_data;
    }

    /**
     * This is a function used in API route
     * 
     * @return
     */
    public function getElectionResults(Request $request)
    {
        $blockchain_communicator = new BlockchainCommunicatorModel();

        $tx_data = [
            'headers' => [
                'tx_hash' => $request['headers']['tx_hash']
            ],
            'tx_details' => [
                'tx_type' => 'request_results'
            ]
        ];
        $tx_data = $blockchain_communicator->sendMessage($tx_data);

        return json_decode($tx_data);
    }

    /**
     * Get transaction
     * 
     * This is a function used in API route
     * 
     * @param Request $request:
     * 
     * @return
     */
    public function decryptor(Request $request)
    {
        $decrypted = [
            'decrypted_data' => [],
            'status' => 'rejected'
        ];

        if (Hash::check($request['decryption_key'], $this->user_info['password'])) {
            $decrypted['decrypted_data'] = $this->decryptData($this->user_info['password'], $request['to_decrypt']);
            $decrypted['decrypted_data'] = json_decode($decrypted['decrypted_data']);
            $decrypted['status'] = 'approved';
        }

        return response()->json($decrypted);
    }

    /**
     * Get transaction
     * 
     * This is a function used in API route
     * 
     * @param Request $request:
     * 
     * @return
     */
    public function addVote(Request $request)
    {
        $blockchain_communicator = new BlockchainCommunicatorModel();

        $vote_data = [
            'headers' => [
                'prev_hash' => $this->getLatestTransaction()->tx_details->specified_tx_details->headers->tx_hash,
                'timestamp' => Carbon::now()->getPreciseTimestamp(3)
            ],
            'tx_details' => [
                'tx_type' => 'add_vote',
                'election' => $request['election'],
                'candidate' => $request['candidate'],
                'voter_details' => $this->encryptData($this->user_info['password'], $this->user_info)
            ]
        ];
        $vote_data['headers']['tx_hash'] = $this->generateHash(json_encode($vote_data));

        $response = $blockchain_communicator->sendMessage($vote_data);
        $response = json_decode($response);

        if ($response->tx_details->status == 'approved') {
            $voted_elections = new VotedElectionsModel();
            $voted_elections->addVotedElection($this->user_info['id'], $vote_data['tx_details']['election'], $vote_data['headers']['tx_hash']);
        }

        return response()->json($response);
    }

    /**
     * Get transaction
     * 
     * This is a function used in API route
     * 
     * @param Request $request:
     * 
     * @return
     */
    public function addElection(Request $request)
    {
        $blockchain_communicator = new BlockchainCommunicatorModel();

        $election_data = [
            'headers' => [
                'prev_hash' => $this->getLatestTransaction()->tx_details->specified_tx_details->headers->tx_hash,
                'timestamp' => Carbon::now()->getPreciseTimestamp(3)
            ],
            'tx_details' => [
                'tx_type' => 'add_election',
                'election_details' => $request->all(),
                'admin_details' => $this->encryptData($this->user_info['password'], $this->user_info)
            ]
        ];
        $election_data['headers']['tx_hash'] = $this->generateHash(json_encode($election_data));

        $response = $blockchain_communicator->sendMessage($election_data);
        $response = json_decode($response);

        return response()->json($response);
    }

    public function recalculateHash(Request $request)
    {
        $response = [
            'validity' => false,
            'recalculated_hash' => ''
        ];
        
        $tx_data = $request->all();
        $original_hash = $tx_data['headers']['tx_hash'];

        unset($tx_data['headers']['tx_hash']);
        unset($tx_data['tx_details']['status']);

        $tx_data = json_encode($tx_data);        
        $response['recalculated_hash'] = $this->generateHash($tx_data);

        if ($response['recalculated_hash'] != $original_hash) { 
            $tx_data = str_replace(':', ': ', $tx_data);
            $tx_data = str_replace(',', ', ', $tx_data);
            $response['recalculated_hash'] = $this->generateHash($tx_data);

            if ($response['recalculated_hash'] != $original_hash) {
                $tx_data = str_replace('"', '\'', $tx_data);
                $response['recalculated_hash'] = $this->generateHash($tx_data);
                
                if ($response['recalculated_hash'] == $original_hash) {
                    $response['validity'] = true;
                }
            } else {
                $response['validity'] = true;
            }
        } else {
            $response['validity'] = true;
        }
        
        return response()->json($response);
    }

    /**
     * Get transaction
     * 
     * This is a general function
     * 
     * @param Request $request:
     * 
     * @return
     */
    private function generateHash($data)
    {
        return hash('sha256', $data);
    }

    /**
     * Get transaction
     * 
     * This is a general function
     * 
     * @param Request $request:
     * 
     * @return
     */
    private function encryptData($encryption_key, $data)
    {
        $data = json_encode([
            'name' => $data['name'],
            'identification_number' => $data['identification_number']
        ]);

        $iv_length = openssl_cipher_iv_length($this->cipher);
        $iv = openssl_random_pseudo_bytes($iv_length);
        $raw_encrypted = openssl_encrypt($data, $this->cipher, $encryption_key, $this->options, $iv);
        $hmac = hash_hmac('sha256', $raw_encrypted, $encryption_key, $as_binary = true);

        $encrypted = base64_encode($iv . $hmac . $raw_encrypted);

        return strtr($encrypted, [
            '/' => '~'
        ]);
    }

    /**
     * Get transaction
     * 
     * This is a general function
     * 
     * @param Request $request:
     * 
     * @return
     */
    private function decryptData($decryption_key, $data)
    {
        $data = strtr($data, [
            '~' => '/'
        ]);
        $data = base64_decode($data);

        $iv_length = openssl_cipher_iv_length($this->cipher);
        $iv = substr($data, 0, $iv_length);
        $hmac = substr($data, $iv_length, $sha2_length = 32);
        $raw_decrypted = substr($data, $iv_length + $sha2_length);

        return openssl_decrypt($raw_decrypted, $this->cipher, $decryption_key, $this->options, $iv);
    }
}

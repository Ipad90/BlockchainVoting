<?php

namespace App\Http\Middleware;

use App\Models\BlockchainCommunicatorModel;

use Closure;

class CheckValidElectionTX
{
    public function handle($request, Closure $next)
    {
        $txid = $request->route('election_txid');

        if ($txid != null) {
            $blockchain_communicator = new BlockchainCommunicatorModel();
            $tx_data = [
                'headers' => [
                    'tx_hash' => $txid
                ],
                'tx_details' => [
                    'tx_type' => 'view_tx'
                ]
            ];
            $tx_data = $blockchain_communicator->sendMessage($tx_data);
            $tx_data = json_decode($tx_data);

            if (isset($tx_data->tx_details->specified_tx_details)) {
                if ($tx_data->tx_details->specified_tx_details->tx_details->tx_type == 'add_election') {
                    return $next($request);
                }
            }
        }

        return redirect('/invalid-election');
    }
}

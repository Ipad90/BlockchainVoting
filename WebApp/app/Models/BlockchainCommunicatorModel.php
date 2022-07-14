<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

use Illuminate\Support\Facades\Log;

class BlockchainCommunicatorModel extends Model
{
    private $tracker_host;
    private $tracker_port;
    private $nodes;

    public function __construct()
    {
        $this->tracker_host = '127.0.0.1';
        $this->tracker_port = 5150;
        $this->nodes = [];
    }

    public function requestNodesFromTracker()
    {
        $request_node_message = [
            'request_type' => 'request_list'
        ];
        $stringed_request_message = json_encode($request_node_message);

        $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Unable to create socket. \n");
        $result = socket_connect($socket, $this->tracker_host, $this->tracker_port) or die("Unable to connect. \n");
        socket_write($socket, $stringed_request_message, strlen($stringed_request_message)) or die ("Unable to send to server. \n");

        return socket_read($socket, 2048);
    }

    public function sendMessage($data)
    {
        $buffer = '';
        $stringed_data = json_encode($data);

        $nodes = $this->requestNodesFromTracker();
        $nodes = json_decode($nodes);
        $nodes = $nodes->peer_list;
        $node_count = count($nodes);

        if ($node_count > 1) {
            $rng = rand(0, count($nodes));
            $nodes = $nodes[$rng];
        } else {
            $nodes = $nodes[0];
        }

        $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Unable to create socket. \n");
        $result = socket_connect($socket, $nodes[0], $nodes[1]) or die("Unable to connect. \n");
        socket_write($socket, $stringed_data, strlen($stringed_data)) or die ("Unable to send to server. \n");

        return socket_read($socket, 2048);
    }
}

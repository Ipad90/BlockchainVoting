<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class Communicator implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    private $tracker_host;
    private $tracker_port;
    private $nodes;
    private $message;

    public function __construct($message)
    {
        $this->tracker_host = '127.0.0.1';
        $this->tracker_port = 5153;
        $this->nodes = [];
        $this->message = $message;
    }

    public function requestNodesFromTracker()
    {
        $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Unable to create socket. \n");
        $result = socket_connect($socket, $this->tracker_host, $this->tracker_port) or die("Unable to connect. \n");
        socket_write($socket, $this->message, strlen($this->message)) or die ("Unable to send to server. \n");
    }

    public function sendMessage($message)
    {
        $buffer = '';

        $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Unable to create socket. \n");
        $result = socket_connect($socket, $this->tracker_host, $this->tracker_port) or die("Unable to connect. \n");
        socket_write($socket, $this->message, strlen($this->message)) or die ("Unable to send to server. \n");

        while (socket_recv($socket, $buffer, 1024, 0) >= 1) {
            // print_r($buffer);
        }

        socket_close($socket);

        return $buffer;
    }
}

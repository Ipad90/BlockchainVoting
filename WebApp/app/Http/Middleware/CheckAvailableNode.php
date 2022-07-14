<?php

namespace App\Http\Middleware;

use App\Models\BlockchainCommunicatorModel;

use Closure;

class CheckAvailableNode
{
    public function handle($request, Closure $next)
    {
        $blockchain_communicator = new BlockchainCommunicatorModel();

        $available_nodes = $blockchain_communicator->requestNodesFromTracker();
        $available_nodes = json_decode($available_nodes);
        $available_nodes = $available_nodes->peer_list;
        $available_nodes = count($available_nodes);

        if ($available_nodes > 0) {
            return $next($request);
        }

        return redirect('/no-available-nodes');
    }
}

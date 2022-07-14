<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

use App\Http\Controllers\BlockchainCommunicationController;
use App\Http\Controllers\VotedElectionsController;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::post('/add_vote', [BlockchainCommunicationController::class, 'addVote']);

Route::post('/add_election', [BlockchainCommunicationController::class ,'addElection']);

Route::post('/get_tx', [BlockchainCommunicationController::class, 'getTransaction']);

Route::post('/get_election_results', [BlockchainCommunicationController::class, 'getElectionResults']);

Route::post('/recalculate_hash', [BlockchainCommunicationController::class, 'recalculateHash']);

Route::post('/decryptor', [BlockchainCommunicationController::class, 'decryptor']);


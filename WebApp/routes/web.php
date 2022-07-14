<?php

use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

use App\Http\Controllers\BlockchainCommunicationController;
use App\Http\Controllers\VotedElectionsController;

Route::get('/', function()
{
    return Inertia::render('Auth/Login', [
        'canLogin' => Route::has('login'),
        'canRegister' => Route::has('register'),
        'laravelVersion' => Application::VERSION,
        'phpVersion' => PHP_VERSION,
    ]);
});

Route::get('/login', function()
{
    return Inertia::render('Auth/Login');
})->name('login');

Route::group(['middleware' => 'auth:sanctum'], function()
{
    Route::group(['middleware' => 'check_available_node'], function()
    {
        Route::get('/', function()
        {
            $elections = new BlockchainCommunicationController();
            $elections = $elections->listElections();
    
            return Inertia::render('Dashboard', ['elections' => $elections]);
        })->name('dashboard');
    
        Route::get('/vote/{election_txid?}', function($election_txid = null)
        {
            $election_data = new BlockchainCommunicationController();
            $election_data = $election_data->getElection($election_txid);

            return Inertia::render('Vote', ['election_data' => $election_data]);
        })->middleware('check_valid_election_tx')->name('vote');
    
        Route::get('/transaction_viewer', function()
        {
            return Inertia::render('TransactionViewer');
        })->name('transaction_viewer');
    
        Route::get('/results', function()
        {
            return Inertia::render('Results');
        })->name('results');
    
        Route::get('/admin', function()
        {
            return Inertia::render('Admin');
        })->middleware(['user_type'])->name('admin');

        Route::get('/invalid-election', function()
        {
            return Inertia::render('Errors/NonElectionTX');
        });
    });

    Route::get('/voted_elections', function()
    {
        $voted_elections = new VotedElectionsController();
        $voted_elections = $voted_elections->getVotedElections();

        return Inertia::render('VotedElections', ['voted_elections' => $voted_elections]);
    })->name('voted_elections');

    Route::get('/no-available-nodes', function()
    {
        return Inertia::render('Errors/NoNodes');
    });
});

require __DIR__.'/auth.php';

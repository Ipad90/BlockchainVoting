<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;

use App\Models\VotedElectionsModel;

class VotedElectionsController extends Controller
{
    public function getVotedElections()
    {
        $voted_elections = new VotedElectionsModel();
        $voted_elections = $voted_elections->getVotedElections(Auth::id());

        return response()->json($voted_elections);
    }
}

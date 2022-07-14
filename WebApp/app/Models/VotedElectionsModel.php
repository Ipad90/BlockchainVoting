<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

use DB;
use Carbon\Carbon;

class VotedElectionsModel extends Model
{
    public $primaryKey = 'id';
    public $timestamps = true;

    protected $table = 'voted_elections';
    protected $fillable = [
        'user_id',
        'election_txid',
        'vote_txid',
        'created_at',
        'updated_at'
    ];

    public function getVotedElections($user_id)
    {
        return DB::table($this->table)
            ->where($this->fillable[0], $user_id)
            ->orderBy($this->fillable[3], 'desc')
            ->get([
                $this->fillable[1],
                $this->fillable[2],
                $this->fillable[3]
            ]);
    }

    public function addVotedElection($user_id, $election_txid, $vote_txid)
    {
        DB::table($this->table)->insert([
            $this->fillable[0] => $user_id,
            $this->fillable[1] => $election_txid,
            $this->fillable[2] => $vote_txid,
            $this->fillable[3] => Carbon::now(),
            $this->fillable[4] => Carbon::now()
        ]);
    }
}

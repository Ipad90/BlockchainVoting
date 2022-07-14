<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('voted_elections', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained('users');
            $table->string('election_txid');
            $table->string('vote_txid');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('voted_elections');
    }
};

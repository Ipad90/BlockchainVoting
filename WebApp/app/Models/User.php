<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

use DB;
use Carbon\Carbon;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;

    public $primaryKey = 'id';
    public $timestamps = true;

    protected $table = 'users';
    protected $fillable = [
        'name',
        'email',
        'password',
    ];
    protected $hidden = [
        'email_verified_at',
        'remember_token',
        'created_at',
        'updated_at'
    ];
    protected $casts = [
        'email_verified_at' => 'datetime',
    ];
}

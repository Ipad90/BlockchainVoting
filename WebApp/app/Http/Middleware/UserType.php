<?php

namespace App\Http\Middleware;

use Illuminate\Support\Facades\Auth;

use Closure;

class UserType 
{
    public function handle($request, Closure $next)
    {
        $user = Auth::user();

        if ($user->user_type == 1) {
            return $next($request);
        }

        return redirect('/');
    }
}

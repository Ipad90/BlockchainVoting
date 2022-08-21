# Decentralized Blockchain Voting
This project is an online voting system, which utilizes blockchain to store
votes and election information. 

<br/>

Blockchain data is stored on all participant nodes throughout the network to prevent data
manipulation. Participating nodes communicate with each other and other modules of this project
such as the tracker server and web server through Transmission Control Protocol (TCP) sockets.

<br/>

Although online voting and electronic voting may not fully solve voting problems faced throughout the world, this project's main purpose is to demonstrate that blockchain can be used for various purposes, and not just for financial purposes.

<br/>

To create genesis block, run the command

<code>
    python -m genesis_blk
</code>

<br/>

## Python
- Tracker server
- Node server

<br/>

## PHP ( Laravel )
- Web Server

<br/>

## JavaScript ( Vue )
- Web Interface

<br/>

## Commands to run program

### Tracker server
<code>
    python -m Tracker.tracker
</code>

<br/>

### Node server
<code>
    python -m Node.node
</code>

<br/>

### Web Server
<pre><code>cd WebApp
php artisan migrate:fresh
php artisan db:seed
php artisan serve
</code></pre>

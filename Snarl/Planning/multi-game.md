MULTI-GAME SERVER INTERACTION:

    * New Command Line arg: --threads -t, Set the maximum number of games allowed to run concurrently. The actual number 

- The server is started the same way, but the server will wait for at most (--clients * --threads) number of connections. 

- Once players are finished connecting either from timeout or all clients connecting, the will creat up to (--threads) games with at most (--clients) no. of players.
    
    - If the actual number of connected clients is not divisible by the number of threads (i.e. --clients=2 --threads=2, and only 3 clients connect instead of the maximun of 4), the first game will have 
        2 players, and the other game will only have 1.

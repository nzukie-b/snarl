How to interact with SNARL:
Start server with ./snarlServer

arguements for the server are listed provided in the assignment description:

    *levels FILE, where FILE is the path and name of a file containing a JSON level specifications as described in Milestone 8. Default is snarl.levels (in the current directory).

    *clients N, where 1 ≤ N ≤ 4 is the maximum number of clients the server should wait for before starting the game. This option determines max_clients in the protocol specification. Default is 4.

    *wait N, where N is the number of seconds to wait for the next client to connect. This option determines reg_timeout. Default is 60.

    *observe – when this option is given, the server should start a local observer to display the progress of the game. (pygame view)

    *address IP, where IP is an IP address on which the server should listen for connections. Default is 127.0.0.1. You can choose to support a hostname (e.g., localhost), but this is not required.

    *port NUM, where NUM is the port number the server will listen on. Default is 45678

MULTI-GAME SERVER INTERACTION:

    * New Command Line arg: --threads -t, Set the maximum number of games allowed to run concurrently. The actual number 

- The server is started the same way, but the server will wait for at most (--clients * --threads) number of connections. 

- Once players are finished connecting either from timeout or all clients connecting, the will creat up to (--threads) games with at most (--clients) no. of players.
    
    - If the actual number of connected clients is not divisible by the number of threads (i.e. --clients=2 --threads=2, and only 3 clients connect instead of the maximun of 4), the first game will have 
        2 players, and the other game will only have 1.



start client with ./snarlClient
arguements for the client are listed provided in the assignment description:

    *address IP, where IP is an IP address the client should connect to. Default is 127.0.0.1. You can choose to support a hostname (e.g., localhost), but this is not required.

    *port NUM, where NUM is the port number the client should connect to. Default is 45678


CLIENT INTERACTION:

- Everything is in the command line
    - Follow the prompts in the command line
    - Provide moves of the format "row, col"
- Player visuals are in ascii data format
    
Memorandum
-
DATE: February 8th, 2021

TO: Manager

FROM: Brandon Nzukie, Blake Hatch

SUBJECT: "Snarl Design"


Components:

What pieces make up a player
* A player has unique name, an inventory of items that the player has picked up, location information of where the player is trying to move to, and possibly health points and how many ahead they can see. 

What pieces make a up a automated adversary
* An adversary has some unique identifier, the layout of all rooms in a level, a decision/pathfinding strategy, and possibly attack points.

What pieces make up the game
* A Game will consist of a Client, such as a player or adversary, and a Server that the participants will interact with. 
* All clients send location information to the server, and receive an updated response, but only the adversary client has receives the level layout.
* The Server will keep track of the position of all participants, the layout of all rooms in a level including items, whether a level's key has been found, player turn order, whether a player has found the exit or has been eaten, and if to continue to the next level or end the game depending on if a player has made it to the exit.

"Who" knows what, and what "Who" uses to communicate
* Players only know what items they are carrying, and their immediate surroundings. They do not have access to the level layout, or the positions of other participants outside their sight range.
* Adversaries do know the position of the players. They do have access to the level layout from the server.
* Communication will be done over a TCP connection using JSON formatted commands.

What common knowledge is necessary
* The Server and Clients need to know the format of all communication they should expect to receive.
* All clients need to have level layout and participant location information. However, for players this information is only displayed if the are within some number of tiles of an object or player/adversary.

Milestones:

1. Plan out design (Currently here)

2. Add basic client functionality with player location in simple environment

3. Add support for up to 4 players in basic environment, also make it so that client only can see limited area 
around them.

4. Add more player data (health, name, etc.) and add environment attributes (keys, items, obstacles, etc)

5. Create an inventory system, add the ability for players to pick up items for their inventory. Also add player win 
condition from key item and exit appearing in the environment after pickup.

6. Add support for multiple adversaries in client, make sure location and data can be modified.

7. Connect client to server, support sending player location and data to the server in proper JSON format.

8. Add player loss condition and adversary win condition.

9. Receive server response and modify location and data of adversaries using the received data, 
    also send player interactions with adversaries from client to server.

10. Receive server response on how environment and player data (ex: health lowered) is changed by adversaries.
Then change environment and player info on client side accordingly.

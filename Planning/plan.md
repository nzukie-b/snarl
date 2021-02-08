Memorandum
-
DATE: February 8th, 2021

TO: Manager

FROM: Brandon Nzukie, Blake Hatch

SUBJECT: "Snarl Design"


Components:

What pieces make up a player
* A player has unique name, an inventory of items that the player has picked up, location information of where the 

What pieces make a up a automated adversary
* 


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
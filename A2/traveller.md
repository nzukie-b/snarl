Implementation Language:
- 
Python, 3.0

This module will provide the services of a route planner through a simple graph network of towns for a role-playing game.

This module will support the operations:
-
- Create town network with named nodes
- Place named character in town
- Query whether a specified character can reach a destinated town without runnign into any other characters

Necessary Modules:
- 
- "json" for parsing JSON objects
- "apgl" A simple python graph library based on "numpy" and "scipy" for operations on simple graphs

Functions:
- 
create_town(name, connected_towns):
- Creates a node with a specified name and a list of towns it is connected to.

place_character(town):
- Places a character on node associated with the town.

query_can_reach(character, town, characters, towns):
- Starting on the node the character is currently on attempt to traverse through towns without hitting character node in characters and reach the node town is on.
- If a path allows successful traversal between nodes without hitting a character, return true.
- If all paths go through a character return false.
# interface specification - Warmup2 Task1
# package traveller
## class Town
- a Town is a node in a TownNetwork that can contain a Character
### Data
- string of name of the Town: name
- boolean of whether there's a character in Town: inTown
- Character represents the character in town if so, null otherwise
### Operation
- the placement of a named character in a town: Takes in a named Character, mark property inTown of this town as true and update character field in Town
- in case of moving the character in the game, need to remove character from the Town. Mark inTown as false and Character as null
- should be provide and updates its field to the TownNetwork so basic getter and setter is necessary here 

## class TownNetwork
- Represents the map of the game, a simple graph of Town 
### Data
- ADjacency List containing Towns represents the simple graph where nodes of it are Town
### Operation
- Takes in a named Town, specify towns connects to the given town in the TownNetwork (edges in the simple graph) to create the Town in the TownNetwork and establish connections to its neighbors
- Takes in a Character and a Town, return a boolean determine whether a specified character can reach a designated town without running into any other characters

## class Character
- a character in the game, can be placed in a Town. Character can block other characters from travelling through the Town they are in.
### Data
- string of name of the Character: name

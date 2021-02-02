Date: 2/02/2021

TO: ??


Memo

Although the specification mentions packages and interfaces, which seems to imply Java, the language wasn't specified so we chose to do our implementation in python 3.

Names for the functions were not specified so here is list of what was used and what it refers to.

place_char: the placement of a named character in a town: Takes in a named Character, mark property inTown of this town as true and update character field in Town

move_char:- in case of moving the character in the game, need to remove character from the Town. Mark inTown as false and Character as null

get_inTown, set_inTown, get_char, set_char: - should be provide and updates its field to the TownNetwork so basic getter and setter is necessary here 

can_move: - Takes in a Character and a Town, return a boolean determine whether a specified character can reach a designated town without running into any other characters


We have a few suggestion to the specifications:

A Character does not need to be in the Town object. Our implementation of the method to query whether a Character can reach a Town requires going though Towns in TownNetwork to find which one contains the provided Character object. If Characters were managed by the TownNetwork then there is no need to look through Towns in the graph to find origin for a path. TownNetwork could handle this by having a field to keep track of a list of key-values with the Character name or object being the key, and the value would be whatever Town, if any, the Character is located in. 
    This would also make it simpler to determine what nodes can be used in a valid path. Values could be gotten from  the list of Character-Town pairs, and know that any path including one of those values would be invalid.

move_char is described under the Town class, but we feel it would make more sense to have it in the TownNetwork class. Assuming that we are only provided a character and town like the arguements for can_move, it is still necessary to go through the nodes in the TownNetwork graph to determine which Town the Character is in. If the above suggestion is implemented then this should also become more efficient to perform.

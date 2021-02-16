Memorandum
-
DATE: February 16th, 2021

TO: Manager

FROM: Brandon Nzukie, Blake Hatch

SUBJECT: "Game State Design"

Game State Data Representation
-
- Update player
    - Change position
        - Update visible area (Server only sends the data in this area depending on the position)
    - Exit level
    - Add picked up item/key to inventory (If individual players end up needing to pick up keys for themselves to open 
    door)
    - Get eaten by adversary/lower health from adversary attack
    - Increment player kill counter (If this is an attribute)

class Player:
    """
    :param new_player_pos: Coord (Coord is made up of an int x and int y)
    :param item_type: String 
    :param new_health: int
    :param adversaries_killed: int
    :return: 
    """
    def change_position(new_player_pos):
        """Move player to new server-designated position on level."""
        
    def update_visible_area(new_player_pos):
        """Updates tile coordinate range visible to the player based on the new location of the player."""
    
    def add_item_to_inventory(item_type):
        """Adds item on tile that the player has moved to, to that player's inventory."""
    
    def check_health_status(new_health):
        """Takes in new health which server has calculated based on whether an attack has taken place, if
        it reaches 0 player's position is set to null and removed from the level."""
    
    def update_kill_count(adversaries_killed):
        """Takes in new aversary kill count from server and updates the player with it. 
        (This method will be used if kill count is kept track of)"""
     
    
    
- Update Adversary
    - Change position
    - Killed by player/lower health from player attack
    - Increment adversary kill counter (If this is an attribute)
    - Check with other adversaries (Coordinate attack)
    
class Adversary:
    """
    :param new_adversary_pos: Coord (Coord is made up of an int x and int y)
    :param new_health: int
    :param players_killed: int
    :return: 
    """
    def change_position(new_adversary_pos):
        """Move adversary to new server-designated position on level."""
    
    def check_health_status(new_health):
        """Takes in new health which server has calculated based on whether an attack has taken place, if
        it reaches 0 adversary's position is set to null and removed from the level."""
    
    def update_kill_count(players_killed):
        """Takes in new player kill count from server and updates the adversary with it. 
        (This method will be used if kill count is kept track of)"""
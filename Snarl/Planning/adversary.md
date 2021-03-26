Class Adversary:
    def __init__(self, id, loc, current_adversary_health, inventory_contents, cardinal_moves_possible):
    self.id = id
    # Coordinate that shows location relative to the origin
    self.loc = loc
    # The visible tiles two grid coordinates away in cardinal or diagonal directions
    self.visible_tiles = visible_tiles
    self.current_adversary_health = current_adversary_health
    self.inventory_contents = inventory_contents
    self.cur_level = cur_level
    self.cur_room = cur_room
    self.cardinal_moves_possible
    
    def move_to_tile(self, move_location):
        """Move to a location within the range allowed by this adversaries cardinal moves."""
       
    def interact_with_tile_contents(self, current_tile_info):
        """Interact with the contents on the current tile if it exists. The interaction will take place in the order
        enemy interaction, key interaction, and exit interaction. Sends this info to game-manager to be handled."""
     
    def choose_id(self, name):
        """Set the id of the current adversary unique to the others"""
    
    def update_info_from_game_manager(new_adversary):
        """Takes in an unpdated version of the adversary from the game-manager and sets the current adversary to these
        values"""
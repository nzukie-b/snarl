Class RuleChecker:
    
    def validatePlayerMovement(gamestate, level, new_player):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""
        
       
    def validateAdversaryMovement(gamestate, level, new_adversary):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""
    
    def checkMoveToTileValidity(player_or_adversary, Tile):
        """Helper for validating movement, checks if tile that player/adversary is attempting to move to is a walkable 
        tile for that player/adversary (some adversaries might be able to move through walls for example). """
    
    def vaildateMovementDistance(new_player_or_adversary, old_player_or_adversary):
        """Helper for validating movements, takes new players position compared to old player/adversary position and 
        checks that the movement is within the cardinal distance relative to the player/adversary movement speed."""
        
    def validate_interaction(gamestate, player_or_adversary, player_or_adversary):
        """Checks validity of interaction between two players/adversaries, interaction is automatically invalid if it
        it between two players."""
    
    def validate_player_attack(gamestate, player, adversary):
        """Helper for interaction validation that checks if the attack from the player to the adversary does 
        the proper amount of damage. Also checks that adversary is removed from gamestate if they are killed 
        by the attack."""
        
    def validate_adversary_attack(gamestate, player, adversary):
        """helper for interaction validation that checks if the attack from the adversary to the player does the 
        proper amount of damage. Also checks that adversary is removed from gamestate if they are killed 
        by the attack."""
     
    def validate_item_interaction(gamestate, player, level):
        """Checks that level items and player inventory have been properly updated after interaction between player 
        and item. (In the case that adversaries can pick up items this would also check that interaction.)
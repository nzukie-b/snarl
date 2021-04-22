SNARL COMBAT:

The combat system works as follows:
    
    * All actors start with 100 health

    * Player and zombie attack power is 50, Ghost attack power is 34 due to their ability to teleport to rooms

    * Players attack by moving onto adversaries during the player's turn and vice-versa. 
    
        * Damage calculation: target.updated_health = target.current_health - attacker.attack_power

    * Once an actor's health reaches 0, they are ejected for the current level, but can return if the game moves to the next level.
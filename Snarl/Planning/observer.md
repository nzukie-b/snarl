Observer local api

class Observable:
    def __init__(self, cur_gamestate, new_gamestate = cur_gamestate) -> None:
        self._observers = []
        current_gamestate = cur_gamestate
        new_gamestate = new_gamestate
    
    def get_new_gamestate():
        """Gets gamestate from game manager and sets new gamestate to rcieved gamestate."""
        
    def register_observers_with_gamestate():
        """Go into gamestate and run down list of players, adversaries, items, doors, and tiles to create
        observers for each component in the gamestate."""
    
    def __register_observer(self, observer, compoennt) -> None:
        """Add component observers to list of observers."""
    
    def notify_observers(self, new_gamestate) -> None:
        """If gamestate and cur_gamestate are different, notify observers of the change and
           set cur gamestate to new one."""

class Observer:
    def __init__(self, observable) -> None:
        observable.register_observer(self)
    
    ***
    def notify(self, observable, *args, **kwargs) -> None:
        """Notify that observer has been registered with the observable."""
        
    def view_gamestate_component(gamestate_component):
        """Takes in gamestate component and calls private helper to handle the specific type
            of component and view it's information.""""
    
    def __handle_view_adversary(gamestate_component):
        """Private component to view information that adversary can see and also interal adversary
        information (Health, attack power, etc)."""
       
    def __handle_view_player(gamestate_component):
        """Private component to view information that player can see and also interal player
        information (Health, attack power, inventory, etc)."""
    
    def __handle_view_item(gamestate_component):
        """Private component to view interal item information (position, in inventory?, interacted with?)."""
    
    def __handle_view_door(gamestate_component):
        """Private component to view interal door information (opened?, is exit?)."""
        
    def __handle_view_tile(gamestate_component):
        """Private component to view interal tile information (is wall, is floor, has item?)."""
        
    def __handle_view_win_condition(gamestate_component):
        """View conditions necessary to achieve win/progress levels conditions for 
        either players or adversaries. Also show what conditions have been met if game has been 
        won by either adversaries or players."""


subject = Observable()
observer = Observer(subject)
subject.notify_observers("test")


UI Mock Up:
-
................................................................................
                                                               Health: <3 <3 <3                 
                                                                                                                           
                                                                                
               @@@@@@@@@@@@@@@@@                                                
               @@@.  &       @@@                                                
               @@@   &       @@@                                                
               @@@@@@@@      @@@                                                
               @@@&& ..      @@@                                                
               @@@@@&&&   @@@@@@                                                
               @@@((((((((@@@@@@                                                
               @@@        @@@                                                   
               @@@        @@@                                                   
               @@@        @@@                                                   
               @@@        @@@                                                   
               @@@((((((((@@@@@@                                                
               @@@     ...   @@@                                                
               @@@  @@@@@@   @@@                                                
               @@@%%...@@@   @@@                                                
               @@@@@ %%/%%@@@@@@                                                
               @@@@@@@@@@@@@@@@@      
...............................................................................

Inventory:
-------------------------------------------------------------------------------
Sword | Shield | Health Potion | Key |
-------------------------------------------------------------------------------


Legend:
-
Adversary: %
Player: &
Item: .
Wall: @
Door: ((((                                          
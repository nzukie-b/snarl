import sys, os
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from common.observer import Observer, Observable


class LocalObservable(Observable):
    def __init__(self, cur_gamestate, new_gamestate=None) -> None:
        self._observers = []
        current_gamestate = cur_gamestate
        new_gamestate = new_gamestate

    def get_new_gamestate(self):
        """Gets gamestate from game manager and sets new gamestate to received gamestate."""

        render_level(Level([room, room1], [hall]))
        render_players(gamestate.players)
        render_adversaries(gamestate.adversaries)

    def register_observers_with_gamestate(self):
        """Go into gamestate and run down list of players, adversaries, items, doors, and tiles to create
        observers for each component in the gamestate."""

    def __register_observer(self, observer, compoennt) -> None:
        """Add component observers to list of observers."""

    def notify_observers(self, new_gamestate) -> None:
        """If gamestate and cur_gamestate are different, notify observers of the change and
           set cur gamestate to new one."""


class LocalObserver(Observer):
    def __init__(self, observable) -> None:
        observable.register_observer(self)
        self.notify(observable, [], [[]])

    def notify(self, observable, *args, **kwargs) -> None:
        """Notify that observer has been registered with the observable."""
        print("Observer has been registered with observable")

    def view_gamestate_component(self, gamestate_component):
        """Takes in gamestate component and calls private helper to handle the specific type of component
        and view it's information."""
        print(str(gamestate_component))

    def __handle_view_adversary(self, gamestate_component):
        """Private component to view information that adversary can see and also interal adversary
        information (Health, attack power, etc)."""
        print(str(gamestate_component))

    def __handle_view_player(self, gamestate_component):
        """Private component to view information that player can see and also interal player
        information (Health, attack power, inventory, etc)."""

    def __handle_view_item(self, gamestate_component):
        """Private component to view interal item information (position, in inventory?, interacted with?)."""

    def __handle_view_door(self, gamestate_component):
        """Private component to view interal door information (opened?, is exit?)."""

    def __handle_view_tile(self, gamestate_component):
        """Private component to view interal tile information (is wall, is floor, has item?)."""

    def __handle_view_win_condition(self, gamestate_component):
        """View conditions necessary to achieve win/progress levels conditions for
        either players or adversaries. Also show what conditions have been met if game has been
        won by either adversaries or players."""
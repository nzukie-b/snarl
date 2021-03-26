from abc import ABC, abstractmethod

#TODO: Observer abstract class


class Observable(ABC):
    def __init__(self, cur_gamestate, new_gamestate=cur_gamestate) -> None:
        self._observers = []
        current_gamestate = cur_gamestate
        new_gamestate = new_gamestate

    @abstractmethod
    def get_new_gamestate(self):
        """Gets gamestate from game manager and sets new gamestate to rcieved gamestate."""

    @abstractmethod
    def register_observers_with_gamestate(self):
        """Go into gamestate and run down list of players, adversaries, items, doors, and tiles to create
        observers for each component in the gamestate."""

    @abstractmethod
    def __register_observer(self, observer, compoennt) -> None:
        """Add component observers to list of observers."""

    @abstractmethod
    def notify_observers(self, new_gamestate) -> None:
        """If gamestate and cur_gamestate are different, notify observers of the change and
           set cur gamestate to new one."""


class Observer(ABC):
    def __init__(self, observable) -> None:
        observable.register_observer(self)

    @abstractmethod
    def notify(self, observable, *args, **kwargs) -> None:
        """
        Notify
        that
        observer
        has
        been
        registered
        with the observable."""

    @abstractmethod
    def view_gamestate_component(self, gamestate_component):
        """Takes in gamestate component and calls private helper to handle the specific type
        of
        component and view
        it
        's information."""

    @abstractmethod
    def __handle_view_adversary(self, gamestate_component):
        """Private component to view information that adversary can see and also interal adversary
        information (Health, attack power, etc)."""

    @abstractmethod
    def __handle_view_player(self, gamestate_component):
        """Private component to view information that player can see and also interal player
        information (Health, attack power, inventory, etc)."""

    @abstractmethod
    def __handle_view_item(self, gamestate_component):
        """Private component to view interal item information (position, in inventory?, interacted with?)."""

    @abstractmethod
    def __handle_view_door(self, gamestate_component):
        """Private component to view interal door information (opened?, is exit?)."""

    @abstractmethod
    def __handle_view_tile(self, gamestate_component):
        """Private component to view interal tile information (is wall, is floor, has item?)."""

    @abstractmethod
    def __handle_view_win_condition(self, gamestate_component):
        """View conditions necessary to achieve win/progress levels conditions for
        either players or adversaries. Also show what conditions have been met if game has been
        won by either adversaries or players."""
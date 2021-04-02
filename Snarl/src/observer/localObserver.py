import sys, os
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from common.observer import Observer, Observable\
from view.view import render_level, render_players, render_adversaries
from model.level import Level


class LocalObservable(Observable):
    def __init__(self, cur_gamestate, new_gamestate=None) -> None:
        self._observers = []
        self.cur_gamestate = cur_gamestate
        self.new_gamestate = new_gamestate

    def get_new_gamestate(self):
        """Gets gamestate from game manager and sets new gamestate to received gamestate."""
        render_level(self.new_gamestate.current_level.rooms, self.new_gamestate.current_level.halls)
        render_players(self.new_gamestate.players)
        render_adversaries(self.new_gamestate.adversaries)
        self.cur_gamestate = self.new_gamestate

    def register_observers_with_gamestate(self):
        """Go into gamestate and run down list of players, adversaries, items, doors, and tiles to create
        observers for each component in the gamestate."""

    def __register_observer(self, observers, component) -> None:
        """Add component observers to list of observers."""
        observers.append(component)

    def notify_observers(self, new_gamestate) -> None:
        """If new_gamestate and cur_gamestate are different, notify observers of the change and
           set cur gamestate to new one."""
        if self.cur_gamestate != self.new_gamestate:
            print("Gamestates are different, updating gamestate")
            self.cur_gamestate = self.new_gamestate


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
        adversaires = gamestate_component['adversaries']
        for cur_adv in adversaires:
            print(cur_adv.id + " info:")
            print("Location: " + str(cur_adv.loc))
            print("Health: " + str(cur_adv.current_adversary_health))
            print("Cardinal Moves Possible: " + str(cur_adv.cardinal_moves_possible))

    def __handle_view_player(self, gamestate_component):
        """Private component to view information that player can see and also interal player
        information (Health, attack power, inventory, etc)."""
        players = gamestate_component['players']
        for cur_pl in players:
            print(cur_pl.name + " info:")
            print("Location: " + str(cur_pl.loc))
            print("Health: " + str(cur_pl.current_player_health))
            print("Visible Tiles: " + str(cur_pl.visible_tiles))
            print("Inventory: " + str(cur_pl.inventory_contents))

    def __handle_view_item(self, gamestate_component):
        """Private component to view interal item information (position, in inventory?, interacted with?)."""
        items = gamestate_component.items
        for item in items:
            print("Item Position: " + str(item))

    def __handle_view_door(self, gamestate_component):
        """Private component to view interal door information (opened?, is exit?)."""
        doors = gamestate_component.doors
        for door in doors:
            print("Door Position: " + str(door))

    def __handle_view_tile(self, gamestate_component):
        """Private component to view interal tile information (is wall, is floor, has item?)."""
        tiles = gamestate_component.tiles
        for tile in tiles:
            print("Tile Position: " + "R: " + str(tile.row) + " C: " + str(tile.col))
            print("Tile is floor?: " + str(not tile.wall))
            print("Tile is wall?: " + str(tile.wall))
            print("Tile has item?: " + str(tile.item is not None))

    def __handle_view_win_condition(self, gamestate_component):
        """View conditions necessary to achieve win/progress levels conditions for
        either players or adversaries. Also show what conditions have been met if game has been
        won by either adversaries or players."""
        if len(gamestate_component.players) == 0:
            print("Adversaries have won.")
        elif not gamestate_component.exit_locked:
            print("Players have won.")
        else:
            print("Game is not over yet.")
import sys
import os
import json


class TravellerServerInterface:
    def __init__(self):
        self.towns = []
        self.characters = []

    def create_town(self, name, connected_towns):
        """Functionality for creating towns goes here."""
        pass

    def place_character(self, town):
        """Functionality for placing character goes here."""
        pass

    def query_can_reach(self, character, town, characters, towns):
        """Functionality for querying whether a character can reach a town goes here."""
        pass


"""
We would have preferred to put this as a method in the interface and have it take in a town and towns, however
we did not have this method in our traveller.md spec therefore we felt we had to add it in here.
"""
def is_in_towns(json_o, travel_serv):
    in_to = False
    for t in travel_serv.towns:
        if t["name"] == json_o["params"]["town"]:
            in_to = True

    return in_to


"""
We would have preferred to put this as a method in the interface and have it take in a character and towns, however
we did not have this method in our traveller.md spec therefore we felt we had to add it in here.
"""
def is_character_placed(json_o, travel_serv):
    c_placed = False
    for t in travel_serv.towns:
        if t["character"] == json_o["params"]["character"]:
            c_placed = True

    return c_placed


def take_json_input(json_str):
    try:
        json_o = json.loads(json_str)
    except json.decoder.JSONDecodeError:
        print_to_stderr("Given invalid JSON")
        quit()

    # print(json_obj['id'])
    return json_o


def handle_command(command, json_obj, roads_run, travel_serv):
    #TODO: Add specific functionality connected to other modules here
    if command == 'roads':
        if not roads_run:
            roads_run = True
        else:
            print_to_stderr("Roads command can only be run once")
            quit()

        # print_to_stderr(json_obj['command'])

        try:
            for obj in json_obj["params"]:
                try:
                    travel_serv.create_town(obj["from"], [obj["to"]])
                    travel_serv.create_town(obj["to"], [obj["from"]])
                    # print_to_stderr("Added town from: " + obj["from"] + " to: " + obj["to"])
                except TypeError:
                    print_to_stderr("Invalid road param structure")
                    quit()
        except KeyError:
            print_to_stderr("Invalid structure no param key")
            quit()
    # NOTE: Place will always output invalid structure as unimplemented interface methods place_character
    # and create town do not actually update towns
    elif command == 'place':
        if not roads_run:
            print_to_stderr("Roads command must be run first")
            quit()
        # print_to_stderr(json_obj['command'])
        try:
            in_towns = is_in_towns(json_obj, travel_serv)

            if in_towns:
                travel_serv.place_character(json_obj["params"]["town"])
            else:
                print_to_stderr("Invalid structure, town does not exist in town network graph")
            # print_to_stderr("character: " + json_obj["params"]["character"] + " town: " + json_obj["params"]["town"])
        except KeyError:
            print_to_stderr("Invalid structure no param key")
    # NOTE: Place will always output invalid structure as unimplemented interface methods place_character
    # and create_town do not actually update towns
    elif command == 'passage-safe?':
        if not roads_run:
            print_to_stderr("Roads command must be run first")
            quit()
        # print_to_stderr(json_obj['command'])
        try:
            in_towns = is_in_towns(json_obj, travel_serv)
            character_placed = is_character_placed(json_obj, travel_serv)

            if in_towns and character_placed:
                travel_serv.query_can_reach(json_obj["params"]["character"], json_obj["params"]["town"],
                                            travel_serv.characters,
                                            travel_serv.towns)
            else:
                print_to_stderr("Invalid structure, town does not exist in town network graph or character has not " +
                                "been placed.")

            # print_to_stderr("character: " + json_obj["params"]["character"] + " town: " + json_obj["params"]["town"])
        except KeyError:
            print_to_stderr("Invalid structure no param key")
    else:
        print_to_stderr("No valid command given")

    return roads_run


def print_to_stderr(*a):
    # Here a is the array holding the objects
    # passed as the arguement of the function
    print(*a, file=sys.stderr)


if __name__ == '__main__':
    roads_has_run = False
    running = True
    traveller_server = TravellerServerInterface()
    while running:
        json_as_str = input()
        # print_to_stderr("Hello World")
        json_obj = take_json_input(json_as_str)
        command = json_obj['command']
        roads_has_run = handle_command(command, json_obj, roads_has_run, traveller_server)
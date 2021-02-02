import sys
import json


def take_json_input(json_str):
    try:
        json_o = json.loads(json_str)
    except json.decoder.JSONDecodeError:
        print_to_stderr("Given invalid JSON")
        quit()

    #print(json_obj['id'])
    return json_o


def handle_command(command, json_obj, roads_run):
    #TODO: Add specific functionality connected to other modules here
    if command == 'roads':
        if not roads_run:
            roads_run = True
        else:
            print_to_stderr("Roads command can only be run once")
            quit()

        print_to_stderr(json_obj['command'])
        try:
            for obj in json_obj["params"]:
                try:
                    print_to_stderr("from: " + obj["from"] + " to: " + obj["to"])
                except TypeError:
                    print_to_stderr("Invalid road param structure")
                    quit()
        except KeyError:
            print_to_stderr("Invalid structure no param key")
            quit()
    elif command == 'place':
        if not roads_run:
            print_to_stderr("Roads command must be run first")
            quit()
        print_to_stderr(json_obj['command'])
        try:
            print_to_stderr("character: " + json_obj["params"]["character"] + " town: " + json_obj["params"]["town"])
        except KeyError:
            print_to_stderr("Invalid structure no param key")
    elif command == 'passage-safe?':
        if not roads_run:
            print_to_stderr("Roads command must be run first")
            quit()
        print_to_stderr(json_obj['command'])
        try:
            print_to_stderr("character: " + json_obj["params"]["character"] + " town: " + json_obj["params"]["town"])
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
    while running:
        json_as_str = input()
        #print_to_stderr("Hello World")
        json_obj = take_json_input(json_as_str)
        command = json_obj['command']
        roads_has_run = handle_command(command, json_obj, roads_has_run)
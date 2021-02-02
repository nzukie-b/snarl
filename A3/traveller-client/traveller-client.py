import sys
import json


def take_json_input(json_str):
    json_obj = json.loads(json_str)
    #print(json_obj['id'])
    return json_obj


def handle_command(command, json_obj):
    #TODO: Add specific functionality connected to other modules here
    if command == 'roads':
        print_to_stderr(json_obj['command'])
        for obj in json_obj["params"]:
            print_to_stderr("from: " + obj["from"] + " to: " + obj["to"])
    elif command == 'place':
        print_to_stderr(json_obj['command'])
        print_to_stderr("character: " + json_obj["params"]["character"] + " town: " + json_obj["params"]["towm"])
    elif command == 'passage-safe?':
        print_to_stderr(json_obj['command'])
        print_to_stderr("character: " + json_obj["params"]["character"] + " town: " + json_obj["params"]["towm"])


def print_to_stderr(*a):
    # Here a is the array holding the objects
    # passed as the arguement of the function
    print(*a, file=sys.stderr)


if __name__ == '__main__':
    json_as_str = input()
    #print_to_stderr("Hello World")
    json_obj = take_json_input(json_as_str)
    command = json_obj['command']
    handle_command(command, json_obj)
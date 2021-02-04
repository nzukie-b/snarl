#!/usr/bin/env python

import socket
import argparse
import json
from traveller_client import take_json_input

parser = argparse.ArgumentParser()
parser.add_argument('tcp_addr', type=str, nargs='?', help='Server address to connect to.', default='127.0.0.1')
parser.add_argument('port', type=int, nargs='?', help='Port to connect to', default=8000)
parser.add_argument('username', type=str, nargs='?', help='How the server will address the user', default='Glorifrir Flintshoulder')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def json_encode(obj):
    return json.dumps(obj).encode('utf-8')

def json_obj_encode(obj):
    return json.dumps(obj.__dict__).encode('utf-8')

class Create_Req:
    def __init__(self, towns, roads):
        self.towns = towns
        self.roads = roads

class Route:
    def __init__(self, origin, dest):
        self.from = origin
        self.to = dest

class Character:
    def __init__(self, name, town):
        self.name = name
        self.town = town

class Query:
    def __init__(self, char, dest):
        self.character = char
        self.destination = dest


def handle_road_network(roads):
    roads_obj = take_json_input(roads)
    command = roads_obj['command']
    town_names = set()
    routes = []
    if command == 'roads':
        try:
            for obj in roads_obj["params"]:
                try:
                    town_names.add(obj["from"])
                    town_names.add(obj["to"])
                    routes.append(Route(obj['from'], obj['to']))
                except TypeError:
                    print("Invalid road param structure")
                    quit()
        except KeyError:
            print("Invalid structure no param key")
            quit()
    else:
        print("No valid command given")
    return Create_Req(town_names, routes)


def handle_place_chars(chars, towns):
    place_obj = take_json_input(chars)
    command = place_obj['command']
    if command == 'place':
        try:
            for obj in place_obj["params"]:
                try:
                    char = obj['character']
                    town = obj['town']
                    if town not in towns:
                        # TODO: work on invalid place request
                        return None
                    return Character(char, town)
                except TypeError:
                    print("Invalid road param structure")
        except KeyError:
            print("Invalid structure no param key")
    else:
        #TODO: Decide how to handle
        return None



def main():
    args = parser.parse_args()
    server_addr = (args.tcp_addr, args.port)
    s.connect(server_addr)
    s.sendall(json_encode(args.username))
    session_id = s.recv(2048)
    print(['the server will call me', args.username])
    user_roads = input()
    create_request = handle_road_network(user_roads)
    towns = create_request.towns
    s.sendall(json_obj_encode(create_request))
    place_loop = True
    while place_loop:
        placing = True
        while placing:
            user_input = input()
            json_obj = take_json_input(user_input)
            if json_obj['command'] == 'passage_safe?':
                placing = False

            if json_obj['command'] == 'place':




    # while True:
        


    print(args)
    s.close()

if __name__ == '__main__':
    main()


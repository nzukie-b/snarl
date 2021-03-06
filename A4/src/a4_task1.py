#!/usr/bin/env python

from os import error
import socket
import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('tcp_addr', type=str, nargs='?', help='Server address to connect to.', default='127.0.0.1')
parser.add_argument('port', type=int, nargs='?', help='Port to connect to', default=8000)
parser.add_argument('username', type=str, nargs='?', help='How the server will address the user',
                    default='Glorifrir Flintshoulder')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Create_Req:
    def __init__(self, towns, roads):
        self.towns = towns
        self.roads = roads


class Route:
    def __init__(self, origin, dest):
        self.origin = origin
        self.to = dest


class Character:
    def __init__(self, name, town):
        self.name = name
        self.town = town


class Query:
    def __init__(self, char, dest):
        self.character = char
        self.destination = dest


class Batch_Req:
    def __init__(self, chars, query):
        self.characters = chars
        self.query = query


class Client_Error:
    def __init__(self, obj):
        self.error = 'not a request'
        self.object = obj


def take_json_input(json_str):
    json_o = None
    try:
        json_o = json.loads(json_str)
    except:
        # print("Given invalid JSON")
        err = Client_Error(json_str)
        print(json.dumps(err.__dict__))
        # quit()
    return json_o


def json_encode(obj):
    return json.dumps(obj).encode('utf-8')


def json_obj_encode(obj):
    return repr(obj).replace('origin', 'from').encode('utf-8')


def stdin_closed(s):
    return s == ''


def connection_closed(res):
    return res == 0


def handle_road_network(roads):
    roads_obj = take_json_input(roads)
    if roads_obj == None:
        return None
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
                    err = Client_Error(roads_obj)
                    print(json.dumps(err.__dict__))
                    # quit()
        except KeyError:
            # print("Invalid structure no param key")
            err = Client_Error(roads_obj)
            print(json.dumps(err.__dict__))
            # quit()
    else:
        # TODO: Double check what this should return
        # print("No valid command given")
        err = Client_Error(roads_obj)
        print(json.dumps(err.__dict__))
    return Create_Req(town_names, routes)


def handle_place_chars(json_obj):
    try:
        for obj in json_obj["params"]:
            try:
                char = obj['character']
                town = obj['town']
                return Character(char, town)
            except TypeError:
                err = Client_Error(json_obj)
                print(json.dumps(err.__dict__))
    except KeyError:
        # print("Invalid structure no param key")
        err = Client_Error(json_obj)
        print(json.dumps(err.__dict__))


def handle_passage_safe(json_obj):
    try:
        for obj in json_obj["params"]:
            try:
                char = obj['character']
                dest = obj['destination']
                return Query(char, dest)
            except TypeError:
                # print("Invalid road param structure")
                err = Client_Error(json_obj)
                print(json.dumps(err.__dict__))
    except KeyError:
        # print("Invalid structure no param key")
        err = Client_Error(json_obj)
        print(json.dumps(err.__dict__))


def main():
    args = parser.parse_args()
    server_addr = (args.tcp_addr, args.port)
    s.connect(server_addr)
    s.sendall(json_encode(args.username))
    res = s.recv(2048)
    place_loop = True
    # recv returns 0 if the connection has been closed
    if connection_closed(res):
        s.close()
        return None
    print(res.decode("ascii"))
    create_request = None
    while create_request == None:
        user_roads = sys.stdin.readline()
        if stdin_closed(user_roads):
            place_loop = False
            break
        create_request = handle_road_network(user_roads)
    s.sendall(json_obj_encode(create_request))
    # processing loop
    while place_loop:
        batch_chars = []
        batch_query = None
        # place_character loop
        while True:
            json_obj = None
            while json_obj == None:
                user_input = sys.stdin.readline()
                if stdin_closed(user_input):
                    place_loop = False
                    break
                json_obj = take_json_input(user_input)
            if place_loop:
                command = json_obj['command']
                # print("command: " + command)
                if command == 'place':
                    try:
                        # print("towns: " + towns)
                        batch_chars.append(handle_place_chars(json_obj, towns))
                    except:
                        err = Client_Error(json_obj)
                        # print(json.dumps(err.__dict__))
                    continue
                elif command == 'passage_safe?':
                    try:
                        batch_query = handle_passage_safe(json_obj)
                        batch_req = Batch_Req(batch_chars, batch_query)
                        s.sendall(json_obj_encode(batch_req))
                        res = s.recv(8192)
                        if connection_closed(res):
                            place_loop = False
                            break
                        print(res.decode('utf-8'))
                    except:
                        err = Client_Error(json_obj)
                        print(json.dumps(err.__dict__))
                        break
                else:
                    err = Client_Error(json_obj)
                    print(json.dumps(err.__dict__))
                    break
            else:
                break
                # Processing loop will terminate after here if place_loop == False | Continue probably isn't neccessary since its the end of the loop
        continue
    s.close()


if __name__ == '__main__':
    main()


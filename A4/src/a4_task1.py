#!/usr/bin/env python

import socket
import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('tcp_addr', type=str, nargs='?', help='Server address to connect to.', default='127.0.0.1')
parser.add_argument('port', type=int, nargs='?', help='Port to connect to', default=8000)
parser.add_argument('username', type=str, nargs='?', help='How the server will address the user', default='Glorifrir Flintshoulder')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def print_to_stdout(*a):
    # Here a is the array holding the objects
    # passed as the arguement of the function
    print(*a, file=sys.stdout)

def take_json_input(json_str):
    try:
        json_o = json.loads(json_str)
    except json.decoder.JSONDecodeError:
        print_to_stdout("Given invalid JSON")
        quit()

    # print(json_obj['id'])
    return json_o

def json_encode(obj):
    return json.dumps(obj).encode('utf-8')

class Create_Req:
    def __init__(self, towns, roads):
        self.towns = towns
        self.roads = roads

def handle_road_network(roads):
    roads_obj = take_json_input(roads)
    command = roads_obj['command']
    town_names = set()
    road_paths = []
    if command == 'roads':
        try:
            for obj in roads_obj["params"]:
                town_names.add(obj["from"])
                town_names.add(obj["to"])
                try:
                    road_paths.append(obj["from"], [obj["to"]])
                except TypeError:
                    print("Invalid road param structure")
                    quit()
        except KeyError:
            print("Invalid structure no param key")
            quit()
    else:
        print("No valid command given")

def main():
    # args = parser.parse_args()
    # server_addr = (args.tcp_addr, args.port)
    # s.connect(server_addr)
    # s.sendall(json_encode(args.username))
    # session_id = s.recv(2048)
    # print(['the server will call me', args.username])
    # user_roads = input()
    # roads_obj = take_json_input(user_roads)
    # #try if

    while True:
        line = sys.stdin.readline()
        print(line)
        if line == '': break

    #print_to_stdout('hi')

    s.close()

if __name__ == '__main__':
    main()


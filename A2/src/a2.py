#!/usr/bin/env python

import sys
import json
import io
from json.decoder import WHITESPACE
import re
import numpy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sum', dest='sum', action='store_true',
                    help="To sum inputed NumJSON")
parser.add_argument('-p', '--product', dest='product', action='store_true',
                    help='To multiply inputed NumJSON')

# Wasn't able to find a python library to easily handle stream json values
# The following code block draws from a stack overflow post to handle stream json values (https://stackoverflow.com/questions/6886283/how-i-can-i-lazily-read-multiple-json-values-from-a-file-stream-in-python)

# CODE BLOCK FROM STACK OVERFLOW #

braces = '{}[]'
whitespace_esc = ' \t'
braces_esc = '\\'+'\\'.join(braces)
balance_map = dict(zip(braces, [1, -1, 1, -1]))
braces_pat = '['+braces_esc+']'
no_braces_pat = '[^'+braces_esc+']*'
until_braces_pat = no_braces_pat+braces_pat


def streaming_find_iter(pat, stream):
    for s in stream:
        while True:
            match = re.search(pat, s)
            if not match:
                yield (False, s)
                break
            yield (True, match.group())
            s = re.split(pat, s, 1)[1]

def simple_or_compound_objs(stream):
    obj = ''
    unbalanced = 0
    for (c, m) in streaming_find_iter(re.compile(until_braces_pat), stream):
        if (c == 0):  # no match
            if (unbalanced == 0):
                yield (0, m)
            else:
                obj += m
        if (c == 1):  # match found
            if (unbalanced == 0):
                yield (0, m[:-1])
                obj += m[-1]
            else:
                obj += m
            unbalanced += balance_map[m[-1]]
            if (unbalanced == 0):
                yield (1, obj)
                obj = ""

def iterload(fp, cls=json.JSONDecoder, **kwargs):
    if (isinstance(fp, io.TextIOBase) or isinstance(fp, io.BufferedIOBase) or
            isinstance(fp, io.RawIOBase) or isinstance(fp, io.IOBase)):
        string = fp.read()
    else:
        string = str(fp)

    decoder = cls(**kwargs)
    idx = WHITESPACE.match(string, 0).end()
    while idx < len(string):
        obj, end = decoder.raw_decode(string, idx)
        yield obj
        idx = WHITESPACE.match(string, end).end()

def streaming_iterload(stream):
    for c, o in simple_or_compound_objs(stream):
        for x in iterload(o):
            yield x

class Output_Obj:
    def __init__(self, obj, total):
        self.object = obj
        self.total = total

# Creates an Output_Obj from the sum of the provided NumJSON
def create_output_obj_sum(x):
    if type(x) == int:  # Number case
        return Output_Obj(x, x)
    elif type(x) == list:  # Array case
        nums = sum([n for n in x if isinstance(n, int)])
        return Output_Obj(x, nums)
    elif type(x) == dict:  # Object Payload case | recurse on payload value
        obj = Output_Obj(x, create_output_obj_sum(x.get('payload')).total)
        return obj

# Creates an Output Obj from the product of the provided NumJSON
def create_output_obj_product(x):
    if type(x) == int:  # Number case
        return Output_Obj(x, x)
    elif type(x) == list:  # Array case
        # numpy library used for array product uses int64 type. It is not JSON serializable by default so we convert into default int type
        nums = int(numpy.prod([n for n in x if isinstance(n, int)]))
        return Output_Obj(x, nums)
    elif type(x) == dict:  # Object Payload case | recurse on payload value
        obj = Output_Obj(x, create_output_obj_product(x.get('payload')).total)
        return obj

def serialize_output_sum(parsed_values):
    # print("PARSED VALUES: {}\n".format(parsed_values))
    res = []
    for x in parsed_values:
        res.append(json.dumps(create_output_obj_sum(x).__dict__))
    return res

def serialize_output_product(parsed_values):
    res = []
    for x in parsed_values:
        res.append(json.dumps(create_output_obj_product(x).__dict__))
    return res

def serialize_output(parsed_values, operation):
    res = []
    if operation == 'sum':
        res = serialize_output_sum(parsed_values)
    elif operation == 'product':
        res = serialize_output_product(parsed_values)
    else:
        #TODO: Change error message | is this even needed?
        print('Invalid operation')
    print(res)

if __name__ == '__main__':
    args = parser.parse_args()
    operation = ''
    if args.sum:
        operation = 'sum'
    elif args.product:
        operation = 'product'
    parsed_values = []
    # f = open('sample_input.txt', 'r')
    for o in streaming_iterload(sys.stdin):
        parsed_values.append(o)
        # print(o)
    serialize_output(parsed_values, operation)

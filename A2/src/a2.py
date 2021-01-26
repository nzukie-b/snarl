#!/usr/bin/env python

import sys
import json
import io
from json.decoder import WHITESPACE
import re
import ijson

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
    obj = ""
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

def create_output_obj_sum(x):
    if type(x) == int:  # Number case
        obj = Output_Obj(x, x)
        # print(json.dumps(obj.__dict__))
        return json.dumps(obj.__dict__)
    elif type(x) == list:  # Array case
        nums = sum([n for n in x if isinstance(n, int)])
        obj = Output_Obj(x, nums)
        # print(json.dumps(obj.__dict__))
        return json.dumps(obj.__dict__)
    elif type(x) == dict:  # Object Payload case | ignore nested vals
        # print('Dict ' + str(x))
        return x

def serialize_output_sum(parsed_values):
    # print("PARSED VALUES: {}\n".format(parsed_values))
    res = []
    for x in parsed_values:
        res.append(create_output_obj_sum(x))
    print(json.dumps(res))


if __name__ == '__main__':
    parsed_values = []
    f = open('sample_input.txt', 'r')
    for o in streaming_iterload(f.readlines()):
        parsed_values.append(o)
        # print(o)
    serialize_output_sum(parsed_values)
    f.close()

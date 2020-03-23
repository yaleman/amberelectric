#!/usr/bin/env python3

""" really basic 'does this work' tests """

import json
from amberelectric import AmberElectric
from config import username, password

API = AmberElectric(username=username, password=password)

if not API.tokens:
    API.auth()

print("#"*100)
print("Price list")
print("#"*100)
print(json.dumps(API.getpricelist(), indent=2))

print("#"*100)
print("Usage Data")
print("#"*100)
print(json.dumps(API.getusage(), indent=2))

print("done")

#!/usr/bin/env python
# pylint: disable-msg=C0103
"""
    Simple python programme which asks for
    name age and Matrikelnummer nummber
"""
import socket
from collections import OrderedDict

BUFFER_SIZE = 1024
HOST = '127.0.0.1'
PORT = 8080


print("Please enter your name")
name = input()

print("Please enter your age")
age = input()

print("Please enter your Matrikelnummer")
matrikelnummer = input()
data = OrderedDict()
data['name'] = name
data['age'] = age
data['matrikelnummer'] = matrikelnummer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(str(data).encode())
response = s.recv(BUFFER_SIZE)
s.close()

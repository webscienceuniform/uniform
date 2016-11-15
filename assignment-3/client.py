#!/usr/bin/env python
# pylint: disable-msg=C0103
"""
    Simple python programme which asks for
    name age and Matrikelnummer nummber
"""
import socket

BUFFER_SIZE = 1024
HOST = '127.0.0.1'
PORT = 8080

print("Enter web url")
url = input()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(url.encode('utf-8'))
response = s.recv(BUFFER_SIZE)
s.close()

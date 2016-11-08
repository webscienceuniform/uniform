# pylint: disable-msg=C0103
""" Simple Web Server in Python
    using socket
"""
import socket
from collections import OrderedDict

HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
while True:
  data = conn.recv(BUFFER_SIZE)
  if not data: break
  info = eval(data)
  for item in info.items():
    print(item[0].title() + " : " + item[1].title())
  conn.send(data)
conn.close()

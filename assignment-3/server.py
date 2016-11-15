# pylint: disable-msg=C0103
""" Simple Web Server in Python
    using socket
"""
import socket
from assignment_3_2 import extract_path_from_url
from assignment_3_2 import extract_query_from_url
from assignment_3_2 import extract_url_and_fragemnt
from assignment_3_2 import extract_domain_and_port_info


HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        break
    raw_url = data.decode('utf-8')
    url, fragment = extract_url_and_fragemnt(raw_url.strip())
    protocal, url_without_protocal = url.split("://")
    domain, s_domain, port = extract_domain_and_port_info(url_without_protocal)
    query, url_without_path = extract_query_from_url(url_without_protocal)
    path = extract_path_from_url(url_without_path)
    print("path: {}".format(path))
    print("domain: {}".format(domain))
    print("subdomain: {}".format(s_domain))
    print("port: {}".format(port))
    print("query: {}".format(query))
    print("protocal: {}".format(protocal))
    print("fragment: {}".format(fragment))
    conn.send(data)
conn.close()

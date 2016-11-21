#!/urs/bin/python
# pylint: disable-msg=C0103
""" Simple http client which downloads resources from url"""
import sys
import socket
from urllib.parse import urlparse
from helper import get_port_number
from helper import url_with_protocal
from helper import is_empty_string
from helper import save_file


def save_downloaded_file(data, file_name, isHeader=False):
    """
    creates required file name to save
    if file name is empty string then index.html is used as default file name
    """
    new_file_name = None
    if not file_name:
        file_name = "index.html"
    if isHeader:
        new_file_name = file_name + '.header'
        print("Header Information \n")
        print(data)
        print('\n')
    else:
        new_file_name = file_name
    save_file(data, new_file_name)


def handle_file_request(s, data, file_name):
    """ handle downloading file from the server"""
    with open(file_name, 'wb') as f:
        f.write(data)
        while True:
            data = s.recv(1024)
            if not data:
                break
            f.write(data)
        print('{} successfully downloaded'.format(file_name))


def handle_http_request(s, data, file_name):
    """ download html files"""
    full_response = data.decode()
    while True:
        data = s.recv(1024)
        result = data.decode()
        if not data:
            break
        full_response += result
    save_downloaded_file(full_response, file_name.split('/')[-1])


def handle_receving_data(s, file_name):
    """ handles the receiving of the data from socket server
    only processed futher if the server sends back 200 OK other wise programe
    will terminate.
    """
    file_name = file_name.split('/')[-1]

    data = s.recv(1024)
    header, result = data.split(b'\r\n\r\n')
    is_status_200_ok = b'200 OK' in header
    is_file_request = b'Content-Type: image/'

    if not is_status_200_ok:
        print(header.decode())
        return False

    save_downloaded_file(header.decode(), file_name, True)

    if is_file_request:
        handle_file_request(s, result, file_name)
    else:
        handle_http_request(s, result, file_name)


def create_socket_server(domain, port):
    """ creates socket server and request the given url"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, port))
    return s


def start_server(clean_url):
    """ entry point of the application """
    url = url_with_protocal(clean_url)
    HOST, DOMAIN, PATH, _, PARAMETERS, FRAGMENTS = urlparse(url)
    PORT = get_port_number(DOMAIN)
    print("Protocal used: {} ".format(HOST))
    org_path = PATH
    if PATH == '':
        PATH = '/'

    if not is_empty_string(PARAMETERS):
        PATH = PATH + '?' + PARAMETERS

    if not is_empty_string(FRAGMENTS):
        PATH = PATH + "#" + FRAGMENTS

    request = "GET " + PATH + " HTTP/1.1\r\nHost:" + DOMAIN + "\r\n\r\n"
    # lets create an INET, STREAMurling socket
    s = create_socket_server(DOMAIN, PORT)
    # lets send request to the server
    s.send(request.encode())
    handle_receving_data(s, org_path)
    s.close()

if __name__ == '__main__':
    input_url = sys.argv[1]
    start_server(input_url)

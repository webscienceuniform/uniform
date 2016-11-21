# pylint: disable-msg=C0103
"""
Helper utility librabry for httpclient.py

"""


def save_file(data, file_name):
    """ creates file and write data into it"""
    with open(file_name, 'w+') as f:
        f.write(data)
    print('{} successfully written'.format(file_name))


def is_scheme_present(url):
    """
    return true if and only if :// is present in url
    """
    return url.find("://") > 0


def get_port_number(domain):
    """
    returns the port number if available in given domain info
    otherwise returns default port 80
    """
    port = None
    if domain.find(":"):
        try:
            port = int(domain.split(":")[1])
        except (ValueError, IndexError):
            port = 80
    return port


def url_with_protocal(url):
    """ adds http:// if not present
    """
    if not is_scheme_present(url):
        return 'http://' + url
    return url


def url_without_port(protocal):
    """ returns protocal without port number"""
    return protocal.split(":")[0]


def is_empty_string(string):
    """ returns True iff string is empty"""
    return string == ''


def is_status_sucess(status_text):
    """ returns whether 200 OK is present or not"""
    infos = status_text.split("\n")[0]
    return '200' in infos

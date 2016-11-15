# pylint: disable-msg=C0103
"""
Exploring more DNS
"""


def extract_url_and_fragemnt(input_url):
    """ extract fragment from the url
    return fragment and url without fragment
    """
    clean_url = None
    frag = None
    if input_url.find("#") > 0:
        clean_url, frag = input_url.split("#", 1)
    else:
        clean_url = input_url
    return (clean_url, frag)


def extract_query_from_url(input_url):
    """ extract query from the url
    returns query and url with out query
    if query is not present the empty string
    is returned
    """
    query_path = ''
    without_path = input_url
    if input_url.find("?") > 0:
        without_path, query_path = input_url.split("?")
    return(query_path, without_path)


def extract_domain_and_subdomain(raw_domain):
    """
    extract domain and sub domain name
    from given url and returns it
    """
    sub_domain_inner = None
    main_domain = None
    splitted_domain = raw_domain.split(".")
    if splitted_domain[0] == "www":
        main_domain = raw_domain
    else:
        sub_domain_inner = splitted_domain[:1][0]
        main_domain = ".".join(splitted_domain[1:])
    return(main_domain, sub_domain_inner)


def extract_domain_and_port_info(input_path):
    """
    extract full domain name and port number
    from given url and returns it
    """
    inner_port = None
    # determine if there is inner_port
    if input_path.find(":") > 0:
        rawdomain, rawport = input_path.split(":")
        if rawport.find("/"):
            rawport = rawport.split("/")
            try:
                inner_port = int(rawport[0])
            except AttributeError:
                inner_port = None
    # sometimes there won't be inner_port
    elif input_path.find("/") > 0:
        rawdomain = input_path.split("/")[0]
    else:
        rawdomain = input_path
    main_domain, inner_sub_domain = extract_domain_and_subdomain(rawdomain)
    return (main_domain, inner_sub_domain, inner_port)


def extract_path_from_url(input_url):
    """ extract input_path from given url
    and returns path and url without path
    """
    clean_url = input_url.split("://", 1)[0]
    if clean_url.find('/') >= 0:
        return "/" + clean_url.split("/", 1)[1]
    return ''

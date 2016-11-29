import re
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse

from crawl_helper import find_link_tag
from crawl_helper import url_path
from crawl_helper import build_url
from crawl_helper import is_internal_link
from crawl_helper import save_html

from linkqueue import LinkQueue


# some global variables to track the information
base_url = None
dead_link_count = 0
internal_link_count = 0
external_link_count = 0
downloaded_links = set()
unique_external_links = set()
unique_internal_links = set()
dead_links = set()
pages = list()

current_iteration = None
links_to_visit = LinkQueue()


def clean_url(url):
    if url.startswith('http://'):
        return url
    return build_url(base_url, url)

def html_path(path):
    splitted_path = path.split("/")
    return '/'.join(splitted_path[:-1])

def download_html(url):
  try:
    html = urlopen(url)
  except HTTPError as e:
    return None
  return html

def process_url(url):
    global internal_link_count, external_link_count, unique_internal_links
    global dead_link_count, dead_links, unique_external_links, links_to_visit
    print('processing {}'.format(url))
    html = download_html(url)
    if html is None:
        dead_link_count += 1
        dead_links.add(url)
        return False
    html  = html.read().decode()
    save_html(url, html)

    links = list(map(lambda x: x.group(0), find_link_tag(html)))
    urls  = list(map(lambda x: url_path(x), links))
    urls  = list(map(lambda url: clean_url(url), urls))
    internal_links = list(filter(lambda url: is_internal_link(base_url, url), urls))
    internal_link_count += len(internal_links)
    iterable_links = (set(internal_links)).difference(unique_internal_links).difference(dead_links)

    unique_internal_links = unique_internal_links.union(set(internal_links))
    external_links = list(filter(lambda url: not is_internal_link(base_url, url), urls))
    external_link_count += len(external_links)
    unique_external_links = unique_external_links.union(set(external_links))

    for item in iterable_links:
        links_to_visit.put(item, 1)


def main(url):
    global links_to_visit
    links_to_visit.put(url, 1)
    try:
        while not links_to_visit.empty():
            url = links_to_visit.get()
            process_url(url)
    except Exception as e:
        print(e)
    print("Total Dead Links is {}".format(dead_link_count))
    print("Total External Links is {}".format(external_link_count))
    print("Total Internal Links is {}".format(internal_link_count))
    print("Total Internal Unique Links is {}".format(len(unique_internal_links)))
    print("Total External Unique Links is {}".format(len(unique_external_links)))
    print("Total Dead Unique Links is {}".format(len(dead_links)))


if __name__ == "__main__":
  starting_url = 'http://141.26.208.82/articles/g/e/r/Germany.html' # sys.argv[1]
  # http://141.26.208.82/articles/g/e/n/Wikipedia%7EGeneral_disclaimer_3e44.html
  HOST, DOMAIN, PATH, _, PARAMETERS, FRAGMENTS = urlparse(starting_url)
  base_url = HOST + '://' + DOMAIN
  main(starting_url)
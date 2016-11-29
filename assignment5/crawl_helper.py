import re
import os
from urllib.parse import urlparse

base_dir   = os.getcwd()
link_regex = re.compile(r'<a[^>]*>([^<]+)</a>')
href_regex = re.compile(r'href="(.*?)"')

def make_dir(directory):
    os.makedirs(directory, exist_ok=True)

def dir_exists(directory):
    return os.path.exists(directory)

def is_internal_link(domain, link):
    return link.startswith(domain) and link.find(".html") >= 0

def save_html(input_url, html):
    path = urlparse(input_url).path
    splitted_path = path.split("/")
    final_path = '/'.join(splitted_path[:-1])
    if not path.startswith('/'):
        final_path = '/' + final_path
    filename = splitted_path[-1]
    full_path = base_dir + final_path
    if not (dir_exists(full_path)):
        make_dir(full_path)
    with open(full_path + '/' + filename, 'w+') as f:
        f.write(html)

def build_url(domain, url):
    # ../../../../articles/g/o/o/Wikipedia%7EGood_articles_eaa4.html
    return domain + '/' + url.replace('../','')

def find_link_tag(html):
    return list(link_regex.finditer(html))

def url_path(link_tag):
    match = href_regex.search(link_tag)
    href = match.group(0)
    return href[href.find('"') + 1: -1]

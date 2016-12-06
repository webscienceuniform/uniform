# pylint: disable-msg=C0103
import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from download import save_content
from download import download_url
from download import extract_file_name
from download import main

def full_url(domain, path):
    return domain + path

def find_inside_given_id(soup, selector):
    """ find inside the given class"""
    uls = soup.select(selector)
    borrowed_word = set()
    for ul in uls:
        lis = ul.select("li")
        for li in lis:
            a = li.select("a")[0]['href']
            borrowed_word.add(a)

    return list(borrowed_word)

def start(url):
    domain_info = urlparse(url)
    full_domain= domain_info.scheme + "://" + domain_info.netloc
    html = download_url(url)
    if html is not None:
        soup = BeautifulSoup(html.read().decode(), 'html.parser')
        urls = find_inside_given_id(soup, '#mw-content-text')
        internal_links = filter(lambda x: not x.startswith('http://'), urls)
        final = list(map(lambda x: full_url(full_domain, x), internal_links))
        file_name = extract_file_name(url)
        save_content(file_name, str(final))
        for new_url in final:
            main(new_url)


if __name__ == "__main__":
    url = sys.argv[1]
    print(url)
    start(url)
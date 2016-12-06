# pylint: disable-msg=C0103
""" Downloads all the list form given url"""
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup

soup = None
restricted_names = ["place names", "references",
    "see also",
    "Common in South African English",
    "External links"]

def save_content(file_name, content):
    """ save the file with given name and givn content """
    with open(file_name, 'w+') as f:
        f.write(content)
    print('{} written sucessfully'.format(file_name))


def download_url(input_url):
    """ returns html content if request is successful and None for other
    responses"""
    try:
        html = urlopen(input_url)
    except HTTPError:
        return None
    return html


def find_inside_given_id(soup, selector):
    """ find inside the given class"""
    uls = soup.select(selector)
    borrowed_word = set()
    for ul in uls:
        lis = ul.select("li")
        print(lis)
        for li in lis:
            a = li.select("a")[0]
            borrowed_word.add(a.text)

    return borrowed_word


def find_next_to_selector(soup, selector):
    """ find next to the given class name """
    spans = soup.select(selector)
    borrowed_word = set()
    for span in spans:
        if span.string.lower() not in restricted_names:
            uls = span.parent.findNext("ul")
            lis = uls.select("li")
            for li in lis:
                found_workd = li.find("a").text
                borrowed_word.add(found_workd)

            dls = span.parent.findNext("dl")
            if dls is not None:
                dts = dls.select("dt")
                for dt in dts:
                    atags = dt.select("a")
                    for a in atags:
                        borrowed_word.add(a.text)
    return borrowed_word


def process_html(input_html):
    """ process the downloaded html"""
    soup = BeautifulSoup(input_html, 'html.parser')
    spans = soup.select('span.mw-headline')
    length = len(spans)
    print(length)
    if length > 2:
        return find_next_to_selector(soup, 'span.mw-headline')
    else:
        return find_inside_given_id(soup, '#mw-content-text')


def extract_file_name(input_url):
    """returns the required file name extracting from url"""
    path = urlparse(input_url).path
    return path.split('/')[-1].strip() + '.txt'


def main(input_url):
    """ Entry of the programme """
    global restricted_names
    restricted_names = list(map(lambda x: x.lower().strip(), restricted_names))
    html = download_url(input_url)
    if html is not None:
        print("Processing {}".format(input_url))
        html_content = html.read().decode()
        words = list(process_html(html_content))
        file_name = extract_file_name(input_url)
        save_content(file_name, str(words))


if __name__ == "__main__":
    url = 'https://en.wikipedia.org/wiki/List_of_English_words_of_French_origin_(S-Z)'
    main(url)

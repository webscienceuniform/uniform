# pylint: disable-msg=C0103
""" download every image from server"""
import re
import sys
from httpclient import start_server


list_of_images = []
input_file = sys.argv[1]
url = sys.argv[2]
images_with_full_path = []


def img_full_path(img_path, input_url):
    """ build full path of the image
    """
    if img_path.find("://") == -1:
        return input_url.strip() + img_path
    return img_path


with open(input_file, 'r') as f:
    santences = f.read()
    matches = re.findall('src="([^"]+)"', str(santences))
    list_of_images = list(filter(lambda url: url.find('.js') < 0, matches))


for i, img_url in enumerate(list_of_images):
    images_with_full_path.append(img_full_path(img_url, url))


# printing all the url to the console
for i, img_url in enumerate(images_with_full_path):
    print(img_url)

# download every file
for i, img_url in enumerate(images_with_full_path):
    start_server(img_url)

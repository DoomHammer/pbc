
from http.cookiejar import CookieJar
import urllib.request
import urllib.parse
import zipfile



import random

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


class Downloader(object):

    """
    Authorize into the library, save the zip file and extract it.
    """

    def __init__(self, content_id, config):
        self.content_id = content_id
        self.config = config

    def unzip(self):
        with zipfile.ZipFile(self.config['files']['zipfile_name'], 'r') as zip_file:
            zip_file.extractall(self.config['files']['zipdir'])

    def get_file(self):
        jar = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        opener.addheaders = [('User-agent', 'Lib')]
        urllib.request.install_opener(opener)

        payload = {
            'login': self.config['default']['pbc_login'],
            'password': self.config['default']['pbc_password']
        }

        data = urllib.parse.urlencode(payload)
        d = data.encode('utf-8')
        request = urllib.request.Request(self.config['default']['auth_url'], d)
        response = urllib.request.urlopen(request)
        response2 = urllib.request.urlretrieve(self.config['default']['content_url'] + str(self.content_id) + '/zip/',
                                               self.config['files']['zipfile_name'])
        self.unzip()

    def get_thumbnail(self):
        print("Getting the thumbnail...")
        url = "%s%s" % (self.config['default']['thumbnail_url'], self.content_id)
        urllib.request.urlretrieve(url, self.config['files']['jpg_path'])
        return self.config['files']['jpg_path']


"""
class ImageDownloader(object):

    def __init__(self, config):
        self.url = config['default']['url']
        self.image_path = config['files']['image_path']
        self.metadata_url_part = config['default']['metadata_url']
        self.thumbnail_url = config['default']['thumbnail_url']
        self.jpg_path = config['files']['jpg_path']

    def get_images_list(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links_list = soup.find_all('a')
        image_list = []
        for link in links_list:
            href = link.get('href')
            if "edition" in href:
                image_list.append(href)

        return image_list

    @staticmethod
    def prepare_download_url(edition_url):
        # convert url from dlibra/editions-content?id=[id] to /Content/[id]
        parsed_url = urllib.parse.urlparse(edition_url)
        attrs = urllib.parse.parse_qs(parsed_url.query)
        content_id = attrs.get('id')[0]
        new_path = '/Content/' + content_id + "/"
        new_url = urllib.parse.ParseResult(scheme=parsed_url.scheme,
                                           netloc=parsed_url.netloc,
                                           path=new_path,
                                           params='',
                                           query='',
                                           fragment='')
        return urllib.parse.urlunparse(new_url)

    def get_random_image(self):
        image_list = self.get_images_list()
        image_index = random.randrange(0, len(image_list))
        url = self.prepare_download_url(image_list[image_index])

        print("Downloading from url", url)
        urllib.request.urlretrieve(url, self.image_path)
        return self.image_path, image_index

    def get_image_metadata(self, image_index):
        url = self.metadata_url_part + str(image_index)
        response = requests.get(url)
        root = ET.fromstring(response.text)
        image_metadata = {}
        for child in root[0]:
            if 'title' in child.tag:
                image_metadata['title'] = child.text
        return image_metadata

    def get_thumbnail(self, content_id):
        print("Getting the thumbnail...")
        url = "%s%s" % (self.thumbnail_url, content_id)
        print(url)
        urllib.request.urlretrieve(url, self.jpg_path)
        return self.jpg_path

    def pretty_print_image_metadata(self, content_id):
        image_metadata = self.get_image_metadata(content_id)
        return image_metadata['title'][:110]
"""
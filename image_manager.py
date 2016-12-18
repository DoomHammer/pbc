# -*- coding: utf-8 -*-

import os
import zipfile

import urllib.request
import urllib.parse
from http.cookiejar import CookieJar


class Downloader(object):

    """
    Authorize into the library, save the zip file and extract it.
    """

    def __init__(self, content_id, config):
        self.content_id = str(content_id)
        self.config = config

    def unzip(self):
        with zipfile.ZipFile(self.config['files']['zipfile'], 'r') as zip_file:
            zip_file.extractall(self.config['files']['zipdir'])

    def get_file(self):
        """
        Download the whole zip of the publication.
        """

        jar = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        opener.addheaders = [('User-agent', 'LibraryMiner')]
        urllib.request.install_opener(opener)

        payload = {
            'login': self.config['default']['pbc_login'],
            'password': self.config['default']['pbc_password']
        }

        data = urllib.parse.urlencode(payload)
        d = data.encode('utf-8')
        request = urllib.request.Request(self.config['default']['auth_url'], d)
        urllib.request.urlopen(request, timeout=60)
        response = urllib.request.urlopen(self.config['default']['content_url'] + self.content_id + '/zip/')

        data = b''
        file_response = response.read()
        while file_response:
            data += file_response
            file_response = response.read()
            if len(data) >= 500**1024:
                del data
                raise Exception("File is too big!")

        with open(self.config['files']['zipfile'], 'wb') as zipfile:
            zipfile.write(data)

            self.unzip()

    def get_thumbnail(self):
        """
        Last resort: just take the thumbnail.
        """

        print("Getting the thumbnail...")
        url = "%s%s" % (self.config['default']['thumbnail_url'], self.content_id)
        urllib.request.urlretrieve(url, self.config['files']['jpg_path'])
        return self.config['files']['jpg_path']


def cleanup(config):

    def del_files(directory):
        [os.remove(os.path.join(directory, f)) for f in os.listdir(directory)]

    try:
        os.remove(config['files']['zipfile'])
        del_files(config['files']['zipdir'])
        del_files(config['files']['imagesdir'])
    except Exception as e:
        print(e)
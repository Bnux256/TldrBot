import requests
import glob
from zipfile import ZipFile
import os

'''
gets zip file - unzips it. create update command. return markdown file or None.  
'''


def update_cache():
    # Downloading Cache
    zipUrl = "https://raw.githubusercontent.com/tldr-pages/tldr-pages.github.io/master/assets/tldr.zip"
    print('Downloading files, please wait')
    zipFile = requests.get(zipUrl)
    print('aaa')
    with open('tldr.zip', 'wb') as file:
        file.write(zipFile.content)
    print('Download complete')

    # Unzipping the file
    print('Unzipping file')
    os.mkdir('tldr')
    with ZipFile('tldr.zip', 'r') as zipFile:
        zipFile.extractall('tldr')


def getMdFile(command):
    """

    """


update_cache()

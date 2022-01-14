import requests
import glob
from zipfile import ZipFile
import os

'''
gets zip file - unzips it. create update command. return markdown file or None.  
'''


def update_cache():
    """
        Downloads and extracts the commands cache.
    """
    # Downloading Cache
    zip_url = "https://raw.githubusercontent.com/tldr-pages/tldr-pages.github.io/master/assets/tldr.zip"
    print('Downloading files, please wait')
    zip_file = requests.get(zipUrl)
    with open('tldr.zip', 'wb') as file:
        file.write(zipFile.content)
    print('Download complete')

    # Unzipping the file
    print('Unzipping file')
    os.mkdir('tldr')
    with ZipFile('tldr.zip', 'r') as zipFile:
        zipFile.extractall('tldr')
    print('Unzip complete')


def get_md_file(command: str) -> None:
    """Gets the md file of a command

    Args:
        command (str): name of input command

    Returns:

    """


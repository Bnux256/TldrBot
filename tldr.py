import requests
import glob
from zipfile import ZipFile
import os
import json
from requests.models import Response

'''
gets zip file - unzips it. create update command. return markdown file or None.  
'''


def update_cache():
    """
    Downloads and extracts the cache.
    """
    # Download Cache
    zip_url = "https://raw.githubusercontent.com/tldr-pages/tldr-pages.github.io/master/assets/tldr.zip"
    print('Downloading files, please wait')
    zip_file: Response = requests.get(zip_url)
    with open('tldr.zip', 'wb') as file:
        file.write(zip_file.content)
    print('Download complete')

    # Unzip the file
    print('Unzipping file')
    os.mkdir('tldr')
    with ZipFile('tldr.zip', 'r') as file:
        file.extractall('tldr')
    print('Unzip complete')

def is_in_cache(input_command: str, platform: str = "common", language: str = None) -> bool:
    """
    Searches the cache and checks if the given command exists.
    param input_command (str): name of input command
    param platform (str): the given platform
    param language (str): the given language
    """
    # loading index.json file from cache
    with open('tldr/index.json') as file:
        cache_index: dict = json.load(file)
    commands: list = cache_index.get('commands')

    '''check if command exists in cache index'''
    # go through the list of dicts of commands
    for command in commands:
        input_command_match: bool = command.get('name') == input_command 
        platform_in_platforms: bool = platform in command.get('platform')
        
        #  if a language is given then we check if command exists in said language
        if language:
            language_in_languages: bool = language in command.get('language') 
        # else we ignore the language
        else:
            language_in_languages: bool = True
        
        # check if current command is a match
        if  input_command_match and platform_in_platforms and language_in_languages:
            return True
    

def get_md_file(input_command: str, platform: str = "common", language: str = None) -> None:
    """
    Gets the path to a md file of the given command. If it doesn't exist, returns None.
    param command (str): name of input command
    param platform (str): the given platform
    param language (str): the given language
    Returns:
    """



    

print(is_in_cache('cd'))
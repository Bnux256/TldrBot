import requests
import glob
from zipfile import ZipFile
import os
import json
from requests.models import Response
import shutil
import logging

PAGES_DIR = 'tldr-pages'


def update_cache() -> None:
    """
    Downloads and extracts the cache.
    yields: messages for user to show progress. 
    """

    # Download Cache
    logging.info('Downloading files, please wait')
    yield 'Downloading files, please wait'
    zip_url = "https://raw.githubusercontent.com/tldr-pages/tldr-pages.github.io/master/assets/tldr.zip"
    zip_file: Response = requests.get(zip_url)
    with open('tldr.zip', 'wb') as file:
        file.write(zip_file.content)
    logging.info('Download complete')
    yield 'Download complete'

    # Unzip the file
    logging.info('Unzipping file')
    yield 'Unzipping file'

    # deleting folder if exists
    if os.path.exists(PAGES_DIR):
        shutil.rmtree(PAGES_DIR)
    os.mkdir(PAGES_DIR)
    with ZipFile('tldr.zip', 'r') as file:
        file.extractall(PAGES_DIR)
    os.remove('tldr.zip') # deleting tldr.zip

    logging.info('Unzip complete')
    yield 'Unzip complete'

    yield 'Cache Updated!'


def is_in_cache(input_command: str, platform: str = "common", language: str = None) -> bool:
    """
    Searches the cache and checks if the given command exists.
    param input_command (str): name of input command
    param platform (str): the given platform
    param language (str): the given language
    returns is_in_cache (bool): if the command exists in cache
    """
   
    # making sure that index.js exists
    if not os.path.exists('tldr-pages/index.json'):
        logging.info("commands index doesn't exist - downloading cache")
        # updating cache
        gen = update_cache()
        for i in range(5):
            next(gen)

    # loading index.json file from cache
    with open('tldr-pages/index.json') as file:
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
        if input_command_match and platform_in_platforms and language_in_languages:
            return True


def get_md(input_command: str, platform: str = "common", language: str = None) -> str or None:
    """
    Gets the path to a md file of the given command. If it doesn't exist, returns None.
    param command (str): name of input command
    param platform (str): the given platform
    param language (str): the given language
    Returns:
    """
    '''Gets the path of the md file'''
    # If command exists in given language we return the md file
    if is_in_cache(input_command, platform, language):
        if language:
            directory_path = os.path.join(PAGES_DIR, ('pages.' + language), platform, (input_command + '.md'))
        else:
            directory_path = os.path.join(PAGES_DIR, ('pages' + (str(language or ''))), platform, (input_command + '.md'))

    # if command doesn't exist in given language we return the english version of command
    elif is_in_cache(input_command, platform):
        return get_md(input_command, platform)

    # if command doesn't exist in language and in platform we will return it in common
    elif is_in_cache(input_command):
        return get_md(input_command)
    else:
        return None

    # return the md file
    with open(directory_path) as file:
        md_file = file.read()

    return md_file


def get_languages() -> list[str]:
    """
    Function returns a list of all languages in TLDR cache
    Returns: list of strings that are tldr Languages
    """
    # ADD TRY EXCEPT!!!
    dirs = os.listdir(PAGES_DIR)
    dirs = [directory for directory in dirs if os.path.isdir(os.path.join(PAGES_DIR, directory)) and directory != 'pages']
    languages = [directory[directory.find('.') + 1:] for directory in dirs]
    languages.append("en")
    # Remove json and license.md
    return languages


def get_platforms() -> list[str]:
    """
    Function returns a list of all platforms
    Returns platforms[str]: list of all
    """
    try:
        return os.listdir(os.path.join(PAGES_DIR, 'pages'))
    except FileNotFoundError:
        return [""]

def get_commands() -> list[str]:
    """
    returns a list of all commands
    """
    # loading index.json file from cache
    with open('tldr-pages/index.json') as file:
        cache_index: dict = json.load(file)
    commands: list = cache_index.get('commands')
    return [dict.get("name") for dict in commands]
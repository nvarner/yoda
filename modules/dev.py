from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import range
from past.utils import old_div
import json
import sys

import pyspeedtest
import requests

from modules.config import get_config_file_paths
from .util import *

GOOGLE_URL_SHORTENER_API_KEY = "AIzaSyCBAXe-kId9UwvOQ7M2cLYR7hyCpvfdr7w"


@click.group()
def dev():
    """
        Dev command group:\n
        contains commands helpful for developers
    """


@dev.command()
def speedtest():
    """
    Run a speed test for your internet connection
    """
    speed_test = pyspeedtest.SpeedTest()

    try:
        ping = speed_test.ping()
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    click.echo('Speed test results:')
    click.echo('Ping: ' + '{:.2f}'.format(ping) + ' ms')

    download_speed = old_div(speed_test.download(), (1024 * 1024))
    click.echo('Download: ' + '{:.2f}'.format(download_speed) + ' Mb/s')

    upload_speed = old_div(speed_test.upload(), (1024 * 1024))
    click.echo('Upload: ' + '{:.2f}'.format(upload_speed) + ' Mb/s')


# code for URL command


def url_shorten(url_to_be_shortened):
    """
    shorten url
    :param url_to_be_shortened: 
    """
    try:
        r = requests.post('https://www.googleapis.com/urlshortener/v1/url?key=' + GOOGLE_URL_SHORTENER_API_KEY,
                          data=json.dumps({
                              'longUrl': url_to_be_shortened
                          }), headers={
                'Content-Type': 'application/json'
            })
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    data = r.json()
    response = 'Here\'s your shortened URL:\n' + data['id']
    click.echo(response)


def url_expand(url_to_be_expanded):
    """
    expander
    :param url_to_be_expanded: 
    """
    try:
        r = requests.get('https://www.googleapis.com/urlshortener/v1/url', params={
            'key': GOOGLE_URL_SHORTENER_API_KEY,
            'shortUrl': url_to_be_expanded
        })
    except requests.exceptions.ConnectionError:
        click.echo('Yoda cannot sense the internet right now!')
        sys.exit(1)

    data = r.json()
    response = 'Here\'s your original URL:\n' + data['longUrl']
    click.echo(response)


def check_sub_command_url(action, url_to_be_expanded_or_shortened):
    """
    command checker for url shortener and expander
    :param action: 
    :param url_to_be_expanded_or_shortened: 
    :return: 
    """
    sub_commands = {
        'shorten': url_shorten,
        'expand': url_expand
    }
    try:
        return sub_commands[action](url_to_be_expanded_or_shortened)
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda url --help" for more info')


@dev.command()
@click.argument('input', nargs=1)
@click.argument('url', nargs=1)
def url(input, url):
    """
        URL shortener and expander\n\n

        Commands:
        shorten: to shorten the given URL
        expand: to expand shortened URL
    """
    _input = str(input)
    _url = str(url)
    check_sub_command_url(_input, _url)


@dev.command()
def hackernews():
    """
    Hacker news top headlines
    """
    _url = 'https://newsapi.org/v2/everything?sources=hacker-news&apiKey=534594afc0d64a11819bb83ac1df4245'
    response = requests.get(_url)
    result = response.json()
    if result['status'] == 'ok':
        for index in range(result['totalResults']):
            click.echo('News-- ' + str(index + 1) + '/' + str(result['totalResults']) + '\n')
            click.echo('Title--  ' + result['articles'][index]['title'])
            click.echo('Description-- ' + result['articles'][index]['description'])
            click.echo('url-- ' + str(result['articles'][index]['url']) + '\n')
            click.echo('Continue? [press-"y"] ')
            c = click.getchar()
            click.echo()
            if c != 'y':
                break
    else:
        click.echo('Error in api')


@dev.command()
def coinflip():
    """
    Flips a coin and displays an outcome
    """
    import random
    side = random.randint(1, 100) % 2
    click.echo('Heads' if side == 1 else 'Tails')


@dev.command()
def keybindings():
    import csv

    keybindings_config_file_path = get_config_file_paths()["KEYBINDINGS_CONFIG_FILE_PATH"]
    keybindings_config_folder_path = get_folder_path_from_file_path(
        keybindings_config_file_path)

    with open(keybindings_config_folder_path + '/firefox.csv') as binding_file:
        csv_reader = csv.reader(binding_file)
        for row in csv_reader:
            click.echo(' '.join(row))

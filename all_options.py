#!/usr/bin/python3
"""Generate config file with all possible choices, except colorschemes."""

import json

from main.utils import read_file

output = {
    'base': 'headless',
    'environment': [str(key) for key in json.loads(read_file('configs/env.json')).keys()],
    'yes': [str(key) for key in json.loads(read_file('configs/yes.json')).keys()],
    'programming': [str(key) for key in json.loads(read_file('configs/programming.json')).keys()],
    'dev': [str(key) for key in json.loads(read_file('configs/dev.json')).keys()],
    'colors': [],
    #'colors': [
    #    key
    #    for key, value in json.loads(read_file('plugins.json')).items()
    #    if 'attributes' in value and 'colorscheme' in value['attributes']],
}

with open('config.json', 'w', encoding='UTF-8') as config:
    config.write(json.dumps(output))

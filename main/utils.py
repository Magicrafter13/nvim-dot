#!/usr/bin/python3
"""General functions shared between my scripts."""

import json


def read_file(filename):
    """Simple file read using with"""
    with open(filename, "r", encoding="UTF-8") as _f:
        return _f.read()


def write_file(filename, data):
    """Simple file write using with"""
    with open(filename, "w", encoding="UTF-8") as _f:
        _f.write(data)


def load_plugins():
    """Loads plugins.json and makes sure it has good data (see comments)"""
    plugins = json.loads(read_file("plugins.json"))
    for pid, val in list(plugins.items()):
        # Ignore comments
        if pid.startswith("_"):
            plugins.pop(pid)
            continue
        # Add attributes key to all plugins
        if "attributes" not in val:
            val["attributes"] = []
        # If plugin is a colorscheme, but doesn't have the colorscheme key
        # (which tells us its vim name), assume its plugin ID is the
        # colorscheme name
        elif "colorscheme" in val["attributes"] and "colorscheme" not in val:
            val["colorscheme"] = pid
    return plugins

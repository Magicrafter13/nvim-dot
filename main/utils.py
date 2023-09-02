#!/usr/bin/python3
"""General functions shared between my scripts."""


def read_file(filename):
    """Simple file read using with"""
    with open(filename, "r", encoding="UTF-8") as _f:
        return _f.read()


def write_file(filename, data):
    """Simple file write using with"""
    with open(filename, "w", encoding="UTF-8") as _f:
        _f.write(data)

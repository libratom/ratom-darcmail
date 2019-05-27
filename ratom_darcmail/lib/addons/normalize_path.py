#!/usr/bin/env python3

import os

IS_HELPER = False


def main(path):
    """ Returns a normalized version of a file @path with a forward slash as the separator. """

    path = os.path.normpath(path)
    if os.altsep == "/":
        path = path.replace(os.sep, os.altsep)
    
    return path
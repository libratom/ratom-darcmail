#TODO: clean up.

import os

IS_HELPER = False

def main(path):

    path = os.path.normpath(path)
    
    # normalize path to "/"'s ... ???
    if os.altsep == "/":
        path = path.replace(os.sep, os.altsep)
    
    return path
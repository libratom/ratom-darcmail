#!/usr/bin/env python3

""" ???

Todo:
    * Looks like this requires an explicit path, so you need to add a default one if not present.
        - Or don't: probably should be explicit.
    * Check input types?
    * Add logging?
"""

# import modules.
import os


def main(obj, destination, prefix=None, suffix=None, charset="utf-8"):
    """ ???

    Args:
        - ???
    
    Returns:
        ???

    Raises:
        - FileExistsError ???
    """

    print(locals()) # TODO: remove.

    # ???
    if os.path.isfile(destination):
        err = "???"
        raise FileExistsError(err)
    
    # ???
    destination_folder = os.path.dirname(destination)
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    # ???
    wmode = "wb" if isinstance(obj, bytes) else "w"
    with open(destination, mode=wmode, encoding=charset) as fopen:
        
        if prefix is not None:
            fopen.write(prefix) # TODO: assuming everything is writeable are't we? goes for below too.

        for part in obj: #TODO: So if str, bytes, or iterable, you'll just loop? Might be OK.
            fopen.write(part)

        if suffix is not None:
            fopen.write(suffix)

    return

if __name__ == "__main__":
    pass
#!/usr/bin/env python3

""" ???

Todo:
    * Looks like this requires an explicit path, so you need to add a default one if not present.
        - Or don't: probably should be explicit.
    * Check input types?
    * Add logging?
    * If you want to deal with duplicates, this is where to do it: first hash the data, then look
    it up (from a dict in memory, say account.file_dict), if it's a duplicate, return the file path
    that already exists and update the dict with {local_id} = {file path}. If not a duplicate,
    return the path to the new file (and still update that dict).
    * This function should take either bytes, string, or email.message.Message and write the data
    to file. The email object is best because that's how it will look up 
    message.account.duplicate_dict on that item. Bytes/string should just be accepted in cases where
    you need to write something arbitrary to file.
"""

# import modules.
import os

IS_HELPER = True
def main(obj, destination, prefix=None, suffix=None, charset="utf-8"):
    """ ???

    Args:
        - ???
    
    Returns:
        ???

    Raises:
        - FileExistsError ???
    """

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
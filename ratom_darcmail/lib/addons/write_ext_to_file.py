#!/usr/bin/env python3
"""
Todo:
    * If you want to deal with duplicates, this is where to do it: first hash the data, then look
    it up (from a dict in memory, say account.file_dict), if it's a duplicate, return the file path
    that already exists and update the dict with {local_id} = {file path}. If not a duplicate,
    return the path to the new file (and still update that dict).
"""

import logging
import os

IS_HELPER = True

def main(message, darcmail_obj, is_attachment=False,):
    """ Write @message to @destination.

    Args:
        - message (email.message.Message): ???
        - darcmail_obj (darcmail.DarcMail): ???
        - is_attachement (bool): ???
    
    Returns:
        str: The path to the written file.

    Raises:
        - FileExistsError: If @destination already exists.
    """

    # ???
    subdir = darcmail_obj.message_dir if not is_attachment else darcmail_obj.attachment_dir
    ext = ".message" if not is_attachment else ".attachment"

    # ???
    destination = os.path.join(darcmail_obj.eaxs_container, subdir, message.folder.rel_path, 
        "{}{}".format(message.local_id, ext))

    # make sure @destination doesn't exist.
    if os.path.isfile(destination):
        err = "Can't overwrite existing file: {}".format(destination)
        logging.error(err)
        raise FileExistsError(err)
    
    # create diretories as needed.
    destination_folder = os.path.dirname(destination)
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    # write @message to @destination.
    with open(destination, mode="w", encoding=darcmail_obj.charset) as fopen:

        for part in message.as_string():
            fopen.write(part)

    return destination
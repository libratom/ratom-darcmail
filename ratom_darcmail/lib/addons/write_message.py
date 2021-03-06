#!/usr/bin/env python3

"""
Todo:
    * If you want to deal with duplicates, this is where to do it: first hash the data, then look
    it up (from a dict in memory, say account.file_dict), if it's a duplicate, return the file path
    that already exists and update the dict with {local_id} = {file path}. If not a duplicate,
    return the path to the new file (and still update that dict).\
"""

import logging
import os

IS_HELPER = True

def main(msg):
    """ Writes string value of @message to file.

    Args:
        - msg (email.message.Message): The message to write.
    
    Returns:
        str: The path to the written file.

    Raises:
        - FileExistsError: If the file to write already exists.
    """

    # set the output path.
    destination = msg.write_path

    # make sure @destination doesn't exist.
    if os.path.isfile(destination):
        err = "Can't overwrite existing file: {}".format(destination)
        logging.error(err)
        raise FileExistsError(err)
    else:
        logging.info("Writing file: {}".format(destination))
    
    # if needed, create parent directories for file.
    destination_folder = os.path.dirname(destination)
    if not os.path.isdir(destination_folder):
        logging.debug("Creating parent folders: {}".format(destination_folder))
        os.makedirs(destination_folder)

    # write @msg to @destination.
    
    # TODO: Might need a try/except around this: You can update the msg's @parse_errors list if needed.
    
    # TODO: Are you sure about using xmlcharrefreplace for the @errors? What should it be? Optional?

    # TODO: This still includes the Content Type headers and such. Are you supposed to retain that? I doubt it.
        # So might have to start only where there's just been a double line break but remember it might not be "\n\n".
    with open(destination, mode="w", encoding=msg.folder.account.darcmail.charset, 
        errors="xmlcharrefreplace") as fopen:

        for part in msg.walk():
            part = part.as_string()
            fopen.write(part)

    # TODO: figure out what you want to return!
    destination = os.path.relpath(msg.write_path, msg.folder.account.darcmail.eaxs_container)
    return destination
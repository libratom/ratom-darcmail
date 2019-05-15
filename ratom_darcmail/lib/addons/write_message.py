#!/usr/bin/env python3

"""
Todo:
    * If you want to deal with duplicates, this is where to do it: first hash the data, then look
    it up (from a dict in memory, say account.file_dict), if it's a duplicate, return the file path
    that already exists and update the dict with {local_id} = {file path}. If not a duplicate,
    return the path to the new file (and still update that dict).\
    * Now that you've added the "write_path" concept to MessageObject, you'll need to update this
    to reflect that.
"""

import logging
import os

IS_HELPER = True

def main(message, is_attachment=False):
    """ Writes string value of @message to file.

    Args:
        - message (email.message.Message): The message to write.
        - is_attachement (bool): Use True to write to @darcmail_obj.message_dir. Otherwise, use
        False to write to @darcmail_obj.attachment_dir. 
    
    Returns:
        str: The path to the written file.

    Raises:
        - FileExistsError: If the file to write already exists.
    """

    # determine file path and extension.
    subdir = (message.folder.account.darcmail.message_dir if not is_attachment else 
        message.folder.account.darcmail.attachment_dir)
    ext = "msg" if not is_attachment else "att"

    # set file path.
    destination = os.path.join(message.folder.account.darcmail.eaxs_container, subdir,
        message.folder.rel_path, "{}_{}.{}".format(message.folder.account.global_id, 
        message.local_id, ext))

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

    # write @message to @destination.
    # TODO: Might need a try/except around this: You can update the message's @parse_errors list if needed.
    # TODO: Are you sure about using xmlcharrefreplace for the @errors? What should it be? Optional?
    with open(destination, mode="w", encoding=message.folder.account.darcmail.charset, 
        errors="xmlcharrefreplace") as fopen:

        for part in message.walk():
            part = part.as_string()
            fopen.write(part)

    return destination
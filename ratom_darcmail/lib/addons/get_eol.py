#!/usr/bin/env python3

import logging
import os
from .. import message_object

IS_HELPER = True


def _get_string(data):
    """ Returns a string from the @data object. """
    
    # as needed, get string from a message or a file.
    if isinstance(data, message_object.MessageObject):
        blob = next(data.walk())
        blob = blob.decode(errors="replace")
    elif os.path.isfile(data): #TODO: Are you sure that Python will split the line regardless of line ending?   
        with open(data, "r", newline="") as f:
            for line in f:
                blob = line
                break
    else:
        err = "Can't get EOL for data of type: {}".format(type(data))
        if isinstance(data, str):
            err = "Invalid file path: {}".format(data)
        raise ValueError(err)

    return blob


def main(obj):
    """ Gets the end-of-line value of @obj. This addresses the EAXS <Eol> elements.

    Args:
        - obj (object): This must be a message_object.MessageObject, a path to a file (str), or 
        bytes. 
    
    Returns:
        str: The return value.
        Valid return values are "LF", "CR", and "CRLN". These are respective aliases for "\n",
        "\r", and "\r\n".
    """


    logging.debug("Looking up EOL for: {}".format(obj))

    # assume default EOL.
    eol = "LF"
    
    # get some bytes from @obj.
    blob = None
    try:
        blob = _get_string(obj)
    except ValueError as err:
        logging.error(err)
        raise err
    except Exception as err:
        logging.warning("Unable to get EOL; assuming default: {}".format(eol))
        logging.error(err)
        return eol
        
    # determine the EOL.
    if blob is not None:
        eol_tup = blob[-2], blob[-1]
    
    if eol_tup == ("\r", "\n"):
        eol = "CRLN"
    elif eol_tup[1] == "\r":
        eol = "CR"

    logging.debug("EOL is: {}".format(eol))

    return eol
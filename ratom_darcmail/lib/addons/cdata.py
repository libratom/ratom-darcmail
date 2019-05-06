#!/usr/bin/env python3

import logging
import unicodedata
from lxml.etree import CDATA
from ..addons import escape_cdata

IS_HELPER = False

def main(text):
    """ This custom Jinja2 filter converts wraps @text as CDATA. If needed, ending CDATA blocks are 
    escaped. Also, any XML-illegal line endings are converted to "\n".  

    Args:
        - text (str): The string to alter.

    Returns:
        str: The return value.
    """

    # if needed, fallback to string.
    if text is None:
        logging.debug("Got None for @text; falling back to empty string.")
        return ""
    
    # test is @text is CDATA legal.
    is_legal = True
    try:
        CDATA(text)
    except ValueError as err:
        is_legal = False
        logging.warning("Text is not CDATA legal.")
        logging.error(err)
    
    # if needed, legalize @text.
    if not is_legal:
        logging.info("Making text CDATA legal.")
        for ws in ["\f","\r","\v"]:
            text = text.replace(ws, "\n")
        text = "".join([char for char in text if unicodedata.category(char)[0] != "C" or
            char in ("\t", "\n")])
        
    # escape existing CDATA endings; wrap @text as CDATA.
    text = escape_cdata.main(text)
    text = "<![CDATA[{}]]>".format(text)
    
    return text
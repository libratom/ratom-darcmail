#!/usr/bin/env python3

import logging

IS_HELPER = False

def main(text):
    """ This custom Jinja2 filter escapes any ending CDATA blocks in @text.

    Args:
        - text (str): The string to alter.
    
    Returns:
        str: The return value.
    """

    logging.info("Escaping CDATA ending blocks as needed.")

    # if needed, fallback to string.
    if text is None:
        logging.debug("Got None for @text; falling back to empty string.")
        return ""
    
    # escape ending CDATA block.
    text = text.replace("]]>", "]]&gt;")
    
    return text
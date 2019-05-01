#!/usr/bin/env python3

""" ???

Todo:
    * Check input types?
    * Add logging?
"""


def main(params, restrictions=["id", "name"]):
    """ This is meant to accomodate the elements ... ???

    Args:
        - params (list): ??? email.message.get_params ... If None, ...
        - restrictions (list): ???
    
    Returns:
        list: The return type.
        If @params is None, the list is empty.
    """

    # if @params is None, fallback to an empty list.
    if params is None:
        params = []
    
    # remove items in @params as needed.
    # TODO: Do you also just need a condition to skip it if @value == "" regardless of name? Refer to EAXS to see what's allowed?
    for name, value in params:
        if name.lower() in restrictions or ("/" in name and value == ""):
            params.remove((name, value))

    return params
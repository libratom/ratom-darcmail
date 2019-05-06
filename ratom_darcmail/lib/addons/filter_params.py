#!/usr/bin/env python3

IS_HELPER = True

def main(params, restrictions=["id", "name"]):
    """ Returns a copy of @params in which items are filtered out per @resttrictions. This is meant
    to accomodate EAXS elements such as <ContentTypeParam> that have <Name> and <Value> children in
    which items are omitted if the <Name> value violates certain restrictions.

    Args:
        - params (list): The parameters to filter. Each item is a tuple of name/value pairs. This 
        will be the result of a call to an email.message.Message obeject's get_params() method.
        - restrictions (list): If the first tuple item for a tuple in @params is equal to a lower
        case value in @restrictions, then the tuple will be omitted from the returned copy of 
        @params.
    
    Returns:
        list: The return type.
        If @params is None, the list is empty.
    """

    # if needed, fallback to an empty list.
    if params is None:
        return []

    # filter items in @params as needed.
    filtered_params = []
    for name, value in params:
        if name.lower() not in restrictions and "/" not in name and value not in ["", None]:
            filtered_params.append((name, value))

    return filtered_params
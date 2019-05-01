#!/usr/bin/env python3

""" This dynamically loads all modules in ./eaxs_helpers and adds their API as an attribute to an
object, "EAXSHelpers". This can be imported with "from lib.eaxs_helpers import EAXSHelpers".

Each module file in ./eaxs_helpers is expected to have a "main" function that provides the API. 
For example, EAXSHelpers.close_folders() will be equivalent to the underlying function, 
close_folders.main(). 

Todo:
    * Now that you've added filters, you need to rewrite the docstring and maybe update var names
    and comments, and the name of this folder itself, etc.
"""

# import modules.
import glob as _glob
import importlib as _importlib
import os as _os


def _load_functions_from_files():
    """ Imports all module files. Returns a dict where each key is the module name and the value of
    the key is the module's main() function. """

    # create dicts to return. 
    helpers, filters = {}, {}

    # glob all .py module files.
    _here = _os.path.dirname(__file__)
    _here_modules = _os.path.join(_here, "*.py")

    # add each module and it's main() function to @helpers.
    for file in _glob.glob(_here_modules):

        # skip this __init__.py file.
        if file == __file__:
            continue
        
        # get the module name from the module's file name.
        filename = _os.path.basename(file)
        module, ext = _os.path.splitext(filename)

        # import the module dynamically per: https://stackoverflow.com/a/31285643.
        imported_module = _importlib.import_module("." + module, __name__)

        # ???
        filter_prefix  = "filter__"
        is_filter = True if module.startswith(filter_prefix) else False
        if is_filter:
            module = module[len(filter_prefix):]

        # update @helpers or @filters as needed.
        update_dict = filters if is_filter else helpers
        update_dict[module] = getattr(imported_module, "main")
        
    return (helpers, filters)


# create an object contaning helper functions.
EAXSHelpers, JinjaFilters = _load_functions_from_files()
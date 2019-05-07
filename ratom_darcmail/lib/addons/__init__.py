#!/usr/bin/env python3

""" Provides an API for all package files as an attribute to either "lib.addons.EAXSHelpers" or
"lib.addons.JinjaFilters".

Each module MUST have an "IS_HELPER" boolean and a "main" function that provides the API. If 
@IS_HELPER is True, the module's @main function will be acessible via "lib.addons.EAXSHelpers".
Otherwise, it will be accessible via "lib.addons.JinjaFilters".
"""

# import modules.
import glob as _glob
import importlib as _importlib
import os as _os


def _load_functions_from_files():

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
 
        # update @helpers.
        update_dict = helpers if imported_module.IS_HELPER else filters
        update_dict[module] = imported_module.main
        
    return helpers, filters


# create objects contaning helper functions.
EAXSHelpers, JinjaFilters = _load_functions_from_files()
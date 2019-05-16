#!/usr/bin/env python3

import logging

IS_HELPER = True
#TODO: Rewrite docstrings now that this helps with MultiBody too.
def main(folder, opened_folders, attr="path"):
    """ Looks at the current @folder depth in the context of previously @opened_folders and 
    returns a list of folders to close. This module is designed to accomodate EAXS' use of recursive
    <Folder> elements.

    Args:
        - folder (folder_object.FolderObject): The most recently opened folder within the
        EAXS context.
        - opened_folders (list): The list of non-closed folders within the EAXS context. Note: this
        must be intially passed in as an empty list and it *will* be mutated over time.
        - attr (str): The attribute of @folder that ???
    
    Returns:
        list: The return value.
        Each item in the list is a folder_object.FolderObject that needs to be immediately 
        closed within the EAXS context.
"""

    # assume there are no folders to close.
    folders_to_close = []

    # if the last item in @opened_folders is not a parent of @folder then add it to 
    # @folders_to_close and remove it from @opened_folders.
    for opened in reversed(opened_folders):
        
        # ???
        folder_attr = getattr(folder, attr)
        opened_attr = getattr(opened, attr)

        # ???
        if not folder_attr.startswith(opened_attr):
            folders_to_close.append(opened)
            opened_folders.remove(opened)
    
    # because @folder is still opened, add it to @opened_folders.
    opened_folders.append(folder)

    return folders_to_close

#TODO: Need to change the name of this because it's not just for folders now.
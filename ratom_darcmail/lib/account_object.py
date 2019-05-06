#!/usr/bin/env python3

""" This module contains a class that represents the Account element within the EAXS context.

TODO:
    * Still not sure about ReferencesAccount - it might need it's own class as originally intended.
        - It'll easier to document what it needs to have.
"""

# import modules.
import hashlib
import logging
import os
import time
from ..lib.folder_object import FolderObject


class AccountObject():
    """ A class that represents the Account element within the EAXS context. """


    def __init__(self, path, email_addresses, is_eml, global_id=None, references_account=None, 
        *args, **kwargs):
        """ Sets instance attributes. 
        
        Args:
            - path (str): The path to the EML or MBOX account data.
            - email_addresses (list): Each item is an email address for the account in question.
            Because an account will typically only consist of one address, a string may be passed in
            instead of a list.
            - is_eml (bool): Use True if the account data is in EML format. Use False to indicate an
            MBOX.
            - global_id (str): The unique identifier for the account. This value must be an
            identifier per the xsd:anyURI restriction. If None, this will be auto-generated.
            - references_account (dict): This represents the ReferencesAccount element within the
            EAXS context. It should contain the lowercase keys: "href" (str), 
            "email_addresses" (list), and "ref_type" (str). Values must be compliant with the EAXS
            XSD.

        Attributes:
            ???

        Example:
            ???
        """

        # set logger; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        # convenience functions to clean up path notation.
        self._normalize_sep = lambda p: p.replace(os.sep, os.altsep) if (
                os.altsep == "/") else p
        self._normalize_path = lambda p: self._normalize_sep(os.path.normpath(p))  
        
        # set attributes.
        self.path = self._normalize_path(path)
        self.is_eml = is_eml
        self.email_addresses = ([email_addresses] if not isinstance(email_addresses, list) else
            email_addresses)
        self.global_id = global_id if global_id is not None else self._get_global_id()
        self.references_account = references_account
        self.args, self.kwargs = args, kwargs

        # set unpassed attributes.
        self.current_id = 0 #TODO: should it be this???: -9223372036854775808
        self.folders = self._get_folders()


    def _get_global_id(self):
        """ Returns an auto-generated account identifier. """

        # create string/bytes consisting of the account address and current time.
        id_str = "{}{}".format(self.email_addresses, time.time())
        id_bytes = id_str.encode(errors="ignore")
        
        # hash @id_bytes and prepend a string to it.
        global_id = self.email_addresses[-1].split("@")[-1] + "_" + hashlib.sha256(
            id_bytes).hexdigest()[:7]

        return global_id

    
    def _get_folders(self):
        """ Returns a generator for the folders in @self.path. Each item is a 
        lib.folder_object.FolderObject. """

        # loop through @self.path's folders.
        for dirpath, dirnames, filenames in os.walk(self.path):
            
            # sort folders per: https://stackoverflow.com/a/6670926.
            dirnames.sort()
            
            # yield a FolderObject.
            for dirname in dirnames:
                folder_path = os.path.join(dirpath, dirname)
                folder = FolderObject(self, folder_path)
                yield folder

        return


    def set_current_id(self):
        """ ??? """
        self.current_id += 1
        return self.current_id



if __name__ == "__main__":
    pass
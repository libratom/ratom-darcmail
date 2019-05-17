#!/usr/bin/env python3

""" This module contains a class that represents the Account element within the EAXS context.

Todo:
    * I think we need internal tracking of current_message_id so that a new id doesn't get assigned
    to a message that's already been yielded via repeated called to get_messages(). OR ... there
    needs to be an understanding that one had better do everything they need to with a message
    as soon as it's yielded and store it in their own data structure if they need to re-refer to it.
        - There's no reason you can't create an id incrementer inside the template itself. But I
        still think you'll want a unique ID for each MessageObject but it won't need to be an int so
        you can have submessages have id's in the form "{rootMessageID}_{subMessageID}", etc.
    * Generator methods should start with "gen_" and list methods should start with "list_".
    * How are attachements going to be read if they aren't embedded into the EML/MBOX, i.e. are
    real, external files?
"""

# import modules.
import hashlib
import logging
import os
import time
from ..lib.folder_object import FolderObject


class AccountObject():
    """ A class that represents the Account element within the EAXS context. """


    def __init__(self, darcmail, path, email_addresses, is_eml=True, global_id=None, 
        references_account=None, *args, **kwargs):
        """ Sets instance attributes. 
        
        Args:
            - darcmail (darcmail.DarcMail): The DarcMail object to which this AccountObject belongs.
            - path (str): The path to the EML or MBOX account data.
            - email_addresses (list): Each item is an email address for the account in question.
            Because an account will typically only consist of one address, a string may be passed in
            instead of a list.
            - is_eml (bool): Use True if the account data is in EML format. Use False to indicate an
            MBOX.
            - global_id (str): The unique identifier for the account. This value should be an
            identifier per the xsd:anyURI restriction. If None, this will be auto-generated.
            - references_account (dict): This represents the ReferencesAccount element within the
            EAXS context. It should contain the lowercase keys: "href" (str), 
            "email_addresses" (list), and "ref_type" (str). Values should be compliant with the EAXS
            XSD.

        Attributes:
            - current_id (int): The current account identifier. This is used to get unique local
            identifiers for messages and/or attachments, etc.
        """

        # set logger; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        
        # set attributes.
        self.darcmail = darcmail
        self.path = path
        self.email_addresses = ([email_addresses] if not isinstance(email_addresses, list) else
            email_addresses)
        self.is_eml = is_eml
        self.global_id = global_id if global_id is not None else self._get_global_id()
        self.references_account = references_account
        self.args, self.kwargs = args, kwargs

        # set unpassed attributes.
        self.current_id = 0


    def get_folders(self):
        """ Generator for the folders in @self.path. Each item is a FolderObject. """

        # loop through @self.path's folders.
        for dirpath, dirnames, filenames in os.walk(self.path):
            
            # remove unused var.
            del filenames

            # sort folders per: https://stackoverflow.com/a/6670926.
            dirnames.sort()
            
            # yield a FolderObject.
            for dirname in dirnames:
                folder_path = os.path.join(dirpath, dirname)
                folder = FolderObject(self, folder_path)
                yield folder

        return


    def _get_global_id(self):
        """ Returns a unique account identifier. """

        # create string/bytes consisting of the account address and current time.
        id_str = "{}{}".format(self.email_addresses, time.time())
        id_bytes = id_str.encode(errors="replace")
        
        # get an email address without "@" signs, etc.
        email_prefix = self.email_addresses[0].replace("@", "AT").replace(".", "DOT")
        email_prefix = "".join([c if c.isidentifier() else "_" for c in email_prefix])

        # hash @id_bytes and prepend @email_prefix to it.
        global_id = email_prefix + "_" + hashlib.sha256(id_bytes).hexdigest()[:10]

        return global_id


    def set_current_id(self):
        """ Increments @self.current_id and returns the new value. """
        
        self.current_id += 1        
        return self.current_id


if __name__ == "__main__":
    pass
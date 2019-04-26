#!/usr/bin/env python3

""" This module contains a class that represents a Folder element within the EAXS context.

Todo:
    * Put get_eol() in a new script and let this AND message_object call it.
    * Add mbox() method to get that MBOX metadata.
        - ~mbox_data = {"relpath": filename, "eol": None, "Hash": None}
        - This will need hash and EOL methods that, per above, need to be in another script.
"""

# import modules.
import email
import email.policy
import glob
import hashlib
import logging
import os
from lib.message_object import MessageObject


class FolderObject():
    """ A class that represents a Folder element within the EAXS context. """


    def __init__(self, account, path, file_extension=".eml"):
        """ Sets instance attributes. 
        
        Args:
            - account (lib.account_object.AccountObject): The AccountObject to which this 
            FolderObject belongs.
            - path (str): The path to this folder.
            - file_extension (str): The file extension that EML or MBOX files must have in order for
            messages to be extracted. Pass in an empty string to ignore testing for a given file
            extension.
        
        Attributes:
            - ???
        """

        # set logger; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        # set attributes
        self.account = account
        self.path = self.account._normalize_path(path)
        self.file_extension = file_extension

        # set unpassed attributes.
        self.rel_path = self.account._normalize_path(os.path.relpath(self.path, self.account.path))
        self.basename = os.path.basename(self.path)
        self.get_messages = (self._get_eml_messages if self.account.is_eml else 
            self._get_mbox_messages)


    def get_files(self):
        """ Returns a generator for each file within @self.path provided the file ends with
        @self.file_extension. """

        # loop through files in @self.path.
        for filename in glob.iglob(self.path + "/*.*"):

            # skip non-files.
            if not os.path.isfile(filename):
                continue

            # if needed, skip files with the wrong extension.
            if self.file_extension is not None:
                if not filename.endswith(self.file_extension):
                    continue
            
            filename = self.account._normalize_path(filename)
            yield filename

        return
        

    def _get_eml_messages(self, policy=email.policy.Compat32()):
        """ Returns a generator for each EML file in @self.path. Each item is a 
        lib.message_object.MessageObject. """
        
        # TODO: add try/except.

        # yield a MessageObject for each EML file.       
        for eml in self.get_files():
            with open(eml, "rb") as eml_bytes:
                message = email.message_from_binary_file(eml_bytes, policy=policy)
            message_object = MessageObject(self, eml, message)
            yield message_object
        
        return
    

    def _get_mbox_messages(self):
        """ Returns a generator for each message in each MBOX file in @self.path. Each item is a 
        lib.message_object.MessageObject. """
        
        #TODO: make this do something!
        pass


if __name__ == "__main__":
    pass
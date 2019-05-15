#!/usr/bin/env python3

""" This module contains a class that represents a Folder element within the EAXS context.

Todo:
    * I'm not having success setting the "factory" for MBOX to email.message.EmailMessage so might
    need to make sure both EML and MBOX use email.message.Message. This needs to be documented big
    time.
    * You might want to pass the charset down from the DarcMail object into the email policy.
"""

# import modules.
import email
import email.policy
import glob
import hashlib
import logging
import mailbox
import os
from ..lib.message_object import MessageObject


class FolderObject():
    """ A class that represents a Folder element within the EAXS context. """


    def __init__(self, account, path, file_extension=None, message_policy=email.policy.Compat32(),
        *args, **kwargs):
        """ Sets instance attributes. 
        
        Args:
            - account (lib.account_object.AccountObject): The AccountObject to which this 
            FolderObject belongs.
            - path (str): The path to this folder.
            - file_extension (str): The file extension that EML or MBOX files must have in order for
            messages to be extracted. Pass in an empty string to ignore testing for a given file
            extension.
        
        Attributes:
            - rel_path (str): The relative path of this folder's @path attribute to its 
            @account.path attribute.
            - get_messages (generator): Each item is a lib.message_object.MessageObject that
            corresponds to each message within this folder. This is an alias to either 
            @_get_eml_messages() if @account.is_eml is True or @_get_mbox_messages() is it's False.
        """

        # set logger; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        # set attributes
        self.account = account
        self.path = path
        self.file_extension = file_extension
        self.message_policy = message_policy
        self.args, self.kwargs = args, kwargs

        # set unpassed attributes.
        self.rel_path = os.path.relpath(self.path, self.account.path)
        self.get_messages = (self._get_eml_messages if self.account.is_eml else 
            self._get_mbox_messages)


    def _get_eml_messages(self):
        """ Generator for each EML file in @self.path. Each item is a 
        lib.message_object.MessageObject. """
        
        # yield a MessageObject for each EML file.       
        for eml in self.get_files():
            with open(eml, "rb") as eml_bytes:
                message = email.message_from_binary_file(eml_bytes, _class=email.message.Message,
                policy=self.message_policy)
            message_object = MessageObject(self, eml, message)
            yield message_object
        
        return
    

    def _get_mbox_messages(self):
        """ Generator for each message in each MBOX file in @self.path. Each item is a 
        lib.message_object.MessageObject. Note: this wil increment @self.account.current_id with
        every yield. """
        
        # yield a MessageObject for each MBOX file's messages. 
        for mbox in self.get_files():
            
            mbox_obj = mailbox.mbox(mbox, factory=email.message.Message(
                policy=self.message_policy))
      
            for message in mbox_obj.values():
                message_object = MessageObject(self, mbox, message)
                yield message_object
        
        return


    def get_files(self):
        """ Generator for each file path within @self.path provided the file ends with 
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
            
            yield filename

        return


if __name__ == "__main__":
    pass
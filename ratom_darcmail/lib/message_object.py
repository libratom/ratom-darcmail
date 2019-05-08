#!/usr/bin/env python3

""" This module contains a class that represents a Message element within the EAXS context. 

Todo:
    * Probably want to add documentation here as to why you didn't just subclass 
    email.message.Message - because it helps with intercepting via __getattr__ through which we'll
    update @self.parse_errors.
"""

# import modules.
import email
import logging
import os
#import traceback


class MessageObject():
    """ A class that represents a Message element within the EAXS context. """
    

    def __init__(self, folder, path, email, *args, **kwargs):
        """ Sets instance attributes. 
        
        Args:
            - folder (lib.folder_object.FolderObject): The FolderObject to which this MessageObject
            belongs.
            - path (str): The path to this message's source EML or MBOX file.
            - email (email.message.Message): The message data.
            
        Attributes:
            - account (lib.account_object.AccountObject): The AccountObject to which this 
            MessageObject belongs.
            - rel_path (str): The relative path of this messages's @path attribute to its 
            @account.path attribute.
            - basename (str): The basename of @path.
            - local_id (int): The current @account.current_id after its been incremented by 1.
            - parse_errors (list): Each item is a tuple in which the first item is a Python 
            exception class and the second item is the exception message.
        """

        # set logger; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        # set attributes.
        self.folder = folder
        self.path = path
        self.email = email
        self.args, self.kwargs = args, kwargs

        # set unpassed attributes.
        self.account = self.folder.account
        self.rel_path = self.account._normalize_path(os.path.relpath(self.path, 
            self.folder.account.path))
        self.basename = os.path.basename(self.path)
        self.local_id = self.account.set_current_id()
        self.parse_errors = []


    def __getattr__(self, attr, *args, **kwargs):
        """ This intercepts non-attributes and assumes that the request is for @self.email. This
        allows requests to @self.email to be logged.

        TODO: You need to catch errors and append traceback.format_exc() to @self.parse_errors.
            - BTW: requesting an invalid attribute is NOT a parse error: it's user error/
            - You only need to concern yourself with failed calls to VALID attributes.
        """

        # wrap method requests per: https://stackoverflow.com/a/13776530.
        def wrapper(*args, **kwargs):
            self.logger.debug("Calling @self.email.{} with (args)|{{kwargs}}: {}|{}".format(attr, 
                args, kwargs))
            try:
                return getattr(self.email, attr)(*args, **kwargs) 
            except Exception as err:
                parse_err = err.__class__.__name__, str(err)
                self.parse_errors.append(parse_err)

        # if @attr belongs to @self.email, request the attribute or method. 
        if hasattr(self.email, attr):
            if not callable(getattr(self.email, attr)):
                self.logger.debug("Getting: @self.email.{}".format(attr))
                getattr(self.email, attr)
            else: 
                return wrapper
        else:
            self.logger.warning("Requested invalid attribute: {}".format(attr))
        
        return


    def get_parts(self):
        """ Generator for each part in self.email.walk(). Each yielded part is itself a 
        MessageObject. Note: that will increment @self.account.current_id for every yield. """

        for part in self.email.walk():
            if isinstance(part, (email.message.Message, email.message.EmailMessage)):
                yield MessageObject(self.folder, self.path, part)

        return

    
if __name__ == "__main__":
    pass
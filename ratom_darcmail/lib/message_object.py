#!/usr/bin/env python3

""" This module contains a class that represents a Message element within the EAXS context. 

Todo:
    * Probably want to add documentation here as to why you didn't just subclass 
    email.message.Message - because it helps with intercepting, etc.
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
            - ???
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
        self._normalize_path = self.account._normalize_path
        self.rel_path = self._normalize_path(os.path.relpath(self.path, self.folder.account.path)) #TODO: Do you need this?
        self.basename = os.path.basename(self.path)
        self.local_id = self.account.set_current_id()
        self.email_parts = self._get_email_parts() 
        self.parse_errors = []


    def __getattr__(self, attr, *args, **kwargs):
        """ This intercepts non-attributes and assumes that the request is for @self.email. This
        allows requests to @self.email to be logged.
        TODO: You need to catch errors and append traceback.format_exc() to @self.parse_errors. """
        
        # wrap method requests per: https://stackoverflow.com/a/13776530.
        def wrapper(*args, **kwargs):
            self.logger.debug("Calling @self.email.{} with (args)|{{kwargs}}: {}|{}".format(attr, 
                args, kwargs))
            return getattr(self.email, attr)(*args, **kwargs) 

        # if @attr belongs to @self.email, request the attribute or method. 
        if hasattr(self.email, attr):
            if not callable(getattr(self.email, attr)):
                self.logger.debug("Getting: @self.email.{}".format(attr))
                return getattr(self.email, attr)
            else: 
                return wrapper
        else:
            self.logger.warning("Requested invalid attribute: {}".format(attr))
        
        return


    def _get_email_parts(self):
        """ ??? """

        for part in self.email.walk():
            if isinstance(part, (email.message.Message, email.message.EmailMessage)):
                yield MessageObject(self.folder, self.path, part)

        return

    
if __name__ == "__main__":
    pass
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
import traceback


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
            - rel_path (str): The relative path of this messages's @path attribute to its 
            @folder.account.path attribute.
            - basename (str): The basename of @path.
            - local_id (int): The current @folder.account.current_id after its been incremented by 
            1.
            - parse_errors (list): Each item is a tuple in which the first item is a Python 
            exception type and the second item is the exception traceback.
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
        self.rel_path = self.folder.account.darcmail._normalize_path(os.path.relpath(self.path, 
            self.folder.account.path))
        self.basename = os.path.basename(self.path)
        self.local_id = self.folder.account.set_current_id()
        self.parse_errors = []


    def __getattr__(self, attr, *args, **kwargs):
        """ This intercepts non-attributes, assumes that the request is for @self.email, logs the
        request, and makes the request. If @attr is a method call and raises an exception, then
        @self.parse_errors is updated with a tuple: the exception type and the traceback. """

        # wrap requests per: https://stackoverflow.com/a/13776530.
        def wrapper(*args, **kwargs):
            self.logger.debug("Calling @self.email.{}() with (args)|{{kwargs}}: {}|{}".format(attr,
                args, kwargs))
            try:
                return getattr(self.email, attr)(*args, **kwargs)
            except Exception as err:
                self.logger.error(err)
                parse_err = err.__class__.__name__, traceback.format_exc()
                self.parse_errors.append(parse_err)

        # if @attr belongs to @self.email, request it. 
        if hasattr(self.email, attr):
            if not callable(getattr(self.email, attr)):
                self.logger.debug("Requesting: @self.email.{}".format(attr))
                return getattr(self.email, attr)
            else:
                return wrapper
        else:
            self.logger.warning("Requested invalid attribute: {}".format(attr))
        
        return


    def get_parts(self):
        """ Generator for each part in self.email.walk(). Each yielded part is itself a 
        MessageObject. """

        for part in self.email.walk():
            if isinstance(part, (email.message.Message, email.message.EmailMessage)):
                yield MessageObject(self.folder, self.path, part)

        return

    
if __name__ == "__main__":
    pass
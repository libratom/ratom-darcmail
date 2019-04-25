#!/usr/bin/env python3

""" This module contains a class that represents a Message element within the EAXS context. 

Todo:
    * get_eol() needs to support getting the EOL from a file so it can also support the 
    "Folder/Mbox/Eol" element. So it probably needs to go in an external module. It can just get 
    wrapped here for ease of access and usage (i.e. no params).
"""

# import modules.
import logging
import os
#import traceback


class MessageObject():
    """ A class that represents a Message element within the EAXS context. """
    

    def __init__(self, folder, path, email):
        """ Sets instance attributes. 
        
        Args:
            - folder (lib.folder_object.FolderObject): ???
            - path (str): ???
            - email (email.message.Message): ???
            
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

        # set unpassed attributes.
        self.account = self.folder.account
        self._normalize_path = self.account._normalize_path
        self.rel_path = self._normalize_path(os.path.relpath(self.path, self.folder.account.path)) #TODO: Do you need this?
        self.basename = os.path.basename(self.path)
        self.local_id = self.account.current_message_id = self.account.current_message_id + 1
        self.parse_errors = []


    def __getattr__(self, attr, *args, **kwargs):
        """ This intercepts non-attributes and assumes that the request is for @self.email. This
        allows requests to @self.email to be logged.
        TODO: You need to catch errors and append traceback.format_exc() to @self.parse_errors. """
        
        # wrap method requests per: https://stackoverflow.com/a/13776530.
        def wrapper(*args, **kwargs):
            self.logger.debug("Calling @self.email.{} with args/kwargs: {}/{}".format(attr, 
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


    def get_eol(self):
        """ Gets the end-of-line value of @self.email.
        
        Returns:
            str: The return value.
            Valid return values are "LF", "CR", and "CRLN". These are respective aliases for "\n",
            "\r", and "\r\n".
        """

        self.logger.debug("Looking up message EOL.")

        # assume default EOL.
        eol = "LF"
        
        # walk through one iteration of @self.email.
        # bytes() is used so the actual content can be inspected for the EOL even if the "blob" is
        # itself an email.message.Message object within a multi-part email.
        blob = None
        try:
            blob = next(self.email.walk())
            blob = bytes(blob)
        except Exception as err:
            self.logger.warning("Unable to inspect message for EOL; assuming default: {}".format(
                eol))
            self.logger.error(err)
            return eol
        
        # determine the EOL.
        if blob is not None:
            eol_tup = chr(blob[-2]), chr(blob[-1])

        # determine the EOL.
        if eol_tup == ("\r", "\n"):
            eol = "CRLN"
        elif eol_tup[1] == "\r":
            eol = "CR"

        self.logger.debug("Message EOL is: {}".format(eol))
        return eol

    
if __name__ == "__main__":
    pass
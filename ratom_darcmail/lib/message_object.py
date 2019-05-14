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
from datetime import datetime


class MessageObject():
    """ A class that represents a Message element within the EAXS context. """
    

    def __init__(self, folder, path, email, mpath=None, *args, **kwargs):
        """ Sets instance attributes. 
        
        Args:
            - folder (lib.folder_object.FolderObject): The FolderObject to which this MessageObject
            belongs.
            - path (str): The path to this message's source EML or MBOX file.
            - email (email.message.Message): The message data. Instead of accessing this directly,
            it's better to make the same request via the MessageObject itself. For example,
            '.get("subject")' will equal '.email.get("subject")'. The difference is that the request
            to '.get()' adds some logging statements. Also, this lets @parse_errors be updated if
            the request raises an exception.
            
        Attributes:
            - rel_path (str): The relative path of this messages's @path attribute to its 
            @folder.account.path attribute.
            - basename (str): The basename of @path.
            - local_id (int): The @folder.account.current_id after it's been incremented by 1.
            - parse_errors (list): Requests from @email that raised an exception. Each item is a 
            dict with the keys: "exception_obj" (Exception), "timestamp" (str), 
            "traceback_obj" (traceback), and "traceback_lines" (list of strings).
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
        self.rel_path = os.path.relpath(self.path, self.folder.account.path)
        self.basename = os.path.basename(self.path)
        self.local_id = self.folder.account.set_current_id()
        self.mock_path = self._get_mock_path()
        self.parse_errors = []


    @staticmethod
    def __get_parse_error(err):
        """ Formats @err so that it can be appended to @self.parse_errors.
        
        Args:
            - err (Exception): The error to format.
            
        Returns:
            dict: The return value.
        """
        
        # get traceback from @err; create list of lines in traceback message.
        traceback_obj = err.__traceback__
        traceback_lines = [l.strip() for l in traceback.format_tb(traceback_obj)]
        
        # create dict to return.
        parse_err = {"error_obj": err, 
                "timestamp": datetime.now().isoformat(), 
                "traceback_obj": traceback_obj,
                "traceback_lines": traceback_lines}
       
        return parse_err


    def __getattr__(self, attr, *args, **kwargs):
        """ This intercepts non-attributes, assumes that the request is for @self.email, logs the
        request, and makes the request. If the request raises an exception, then @self.parse_errors
        is updated and None is returned. """

        # wrap attribute requests.
        def _wrap_attr():
            self.logger.debug("Getting attribute @self.email.{}".format(attr))
            try:
                return getattr(self.email, attr)
            except Exception as err:
                self.logger.error(err)
                self.parse_errors.append(self.__get_parse_error(err))

        # wrap method requests per: https://stackoverflow.com/a/13776530.
        def _wrap_method(*args, **kwargs):
            self.logger.debug("Calling method @self.email.{}({},{})".format(attr, args, kwargs))
            try:
                return getattr(self.email, attr)(*args, **kwargs)
            except Exception as err:
                self.logger.error(err)
                self.parse_errors.append(self.__get_parse_error(err))

        # if @attr belongs to @self.email, request it. 
        if hasattr(self.email, attr):
            if not callable(getattr(self.email, attr)):
                return _wrap_attr()
            else:
                return _wrap_method
        else:
            self.logger.warning("@self.email has no attribute: {}".format(attr))
        
        return


    def _get_mock_path(self):
        """ ??? """
    
        # ???
        if self.email.is_multipart():
            sep, tail = "_", self.email.get_content_subtype()
        else:
            sep, tail = ".", "msg"
            disposition =  self.email.get_content_disposition() 
            if disposition not in [None, ""]:
                tail = disposition[:3]
        
        # ???
        tail = "{}{}{}".format(self.local_id, sep, tail)
        mock_path = os.path.join(os.path.split(self.rel_path)[0], tail)

        return mock_path


    def get_parts(self, msg=None, parts=None):
        """ ??? """

        # ???
        if parts is None:
            parts = []
        msg = self if msg is None else msg        
        parts.append(msg)

        # ???
        if msg.email.is_multipart():
            for part in msg.email._payload:
                part = MessageObject(msg.folder, msg.path, part)
                part.mock_path = os.path.join(msg.mock_path, os.path.basename(part.mock_path))
                self.get_parts(part, parts)

        return parts

    
if __name__ == "__main__":
    pass
#!/usr/bin/env python3

""" This module contains a class that represents a Message element within the EAXS context. 

Todo:
    * You should look into adding @self.email.defects to @self.parse_errors if it makes sense.
    * The @write_path attribute is likely overreach. I don't think this class should be making that
    level of determination for a user. Granted, they can throw it away so maybe it's OK. Think about
    it. Maybe keep it and just add the word "proposed" or "suggested" to the docstring.
    * Probably want to add documentation here as to why you didn't just subclass
    email.message.Message - because it helps with intercepting via __getattr__ through which we'll
    update @self.parse_errors.
    * You definitely want to create a logger exclusively for the interceptor: in case you want to
    filter out those logs.
"""

# import modules.
import email
import hashlib
import logging
import os
import string
import traceback
from datetime import datetime


class MessageObject():
    """ A class that represents a Message element within the EAXS context. """
    

    def __init__(self, folder, path, email, *args, **kwargs):
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
            - local_id (int): The @folder.account.current_id after it's been incremented by 1.
            - mock_path (str): A folder-like path that represents the conceptual location of this
            object within self.folder.account. This is useful when @get_submessages() is used
            because it allows one to see the depth relationship of each part.
            - write_path (str): A ready-made file-like output path for @email. This will be
            prepended with @folder.account.darcmail.message_dir if @email is not an attachment.
            Otherwise, it will be prepended with @folder.account.darcmail.attachment_dir.
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
        self.local_id = self.folder.account.set_current_id()
        self.mock_path, self.write_path = self._get_abstract_paths()
        self.parse_errors = []


    @staticmethod
    def _get_parse_error(err):
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
        parse_error = {"error_obj": err, 
            "timestamp": datetime.now().isoformat(), 
            "traceback_obj": traceback_obj,
            "traceback_lines": traceback_lines}
       
        return parse_error


    def __getattr__(self, attr, *args, **kwargs):
        """ This intercepts non-attributes of @self. It then assumes that the request is for 
        @self.email, logs the request, and makes the request. If the request raises an exception,
        then @self.parse_errors is updated and None is returned. None will also be returned if
        @attr is not an attribute or method of @self.email but @self.parse_errors will not be
        affected because calling a non-attribute of @self.email is a user error.
        
        Args:
            - attr (object): The attribute to retrieve or method to call for @self.email.

        Returns:
            object: The return type.
        """

        # wrap attribute requests.
        def _wrap_attr():
            self.logger.debug("Getting attribute @self.email.{}".format(attr))
            try:
                return getattr(self.email, attr)
            except Exception as err:
                self.logger.error(err)
                self.parse_errors.append(self._get_parse_error(err))

        # wrap method requests per: https://stackoverflow.com/a/13776530.
        def _wrap_method(*args, **kwargs):
            self.logger.debug("Calling method @self.email.{}({},{})".format(attr, args, kwargs))
            try:
                return getattr(self.email, attr)(*args, **kwargs)
            except Exception as err:
                self.logger.error(err)
                self.parse_errors.append(self._get_parse_error(err))

        # if @attr belongs to @self.email, request it. 
        if hasattr(self.email, attr):
            if not callable(getattr(self.email, attr)):
                return _wrap_attr()
            else:
                return _wrap_method
        else:
            self.logger.warning("@self.email has no attribute: {}".format(attr))
        
        return


    def _get_abstract_paths(self, msg=None):
        """ Returns values for needed to set @self.mock_path and @self.write_path.

        Args:
            - msg (MessageObject): If left as None, the "mock_path" will be relative to @self. 
            Otherwise, it will be relative to this @msg. The only use of this argument is expected
            to be a call from @self._get_parts(). 
        
        Returns:
            tuple: The return value.
        """

        # create a unique, fixed length filename prefix for "write_path".
        id_bytes = "{}{}".format(datetime.now(), self.local_id).encode(errors="replace")
        id_hash = hashlib.sha256(id_bytes).hexdigest()[:10]

        # determine the extension and path prefix for "write_path".
        if self.email.get_content_disposition() is None:
            ext = "msg"
            write_prefix = self.folder.account.darcmail.message_dir
        else:
            ext = "att"
            write_prefix = self.folder.account.darcmail.attachment_dir

        # create the "mock_path" and "write_path"; make folder-like paths for multipart messages or
        # file-like paths for non-multipart messages.
        sep = "_" if self.email.is_multipart() else "."
        mock_tail = "{}_{}".format(self.local_id, self.email.get_content_type()).replace("/", sep)
        mock_path = os.path.join(self.folder.rel_path, mock_tail)
        write_tail = "{}.{}".format(id_hash, ext)
        write_path = os.path.join(write_prefix, self.folder.rel_path, write_tail)
        
        # if needed, make the "mock_path" relative to @msg.mock_path.
        if msg is not None:
            mock_path = os.path.join(msg.mock_path, os.path.basename(mock_path))

        return mock_path, write_path


    def _get_parts(self, msg=None, parts=None):
        """ Loops through @self.email._payload and returns a list of its message objects. This is
        designed to be called exclusively by @self.get_submessages().
        
        Args:
            - msg (MessageObject): The message to store to @parts. If None, this defaults to
            @self.
            - parts (list): Each item is a MessageObject. If None, a new list is created.

        Returns:
            list: The return value.
            The returned object is @parts.
        """

        # if needed, set @parts as a list and @msg as @self.g
        parts = [] if parts is None else parts
        msg = self if msg is None else msg        
        
        # add @msg to @parts.
        parts.append(msg)

        # if @msg is a multipart message, then send it and @parts to @self_get_parts().
        if msg.email.is_multipart():
            
            # create a new MessageObject for each part; tweaks the @mock_path attribute relative to
            # @msg.
            for msg_part in msg.email._payload:
                msg_part = MessageObject(msg.folder, msg.path, msg_part, parent_msg=self)
                msg_part.mock_path = msg_part._get_abstract_paths(msg)[0]
                self._get_parts(msg_part, parts)

        return parts


    def get_submessages(self):
        """ Gets all the parts in @self.email._payload and converts each part to a MessageObject in
        which the @mock_path attribute is relative to @self.mock_path. Note: the first item in the
        list is the same object as @self.
        
        Returns:
            list: The return value.
        """
        
        return self._get_parts()


if __name__ == "__main__":
    pass
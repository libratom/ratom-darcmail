#!/usr/bin/env python3

""" This module contains a class that creates EAXS files from Jinja2 templates and a source MBOX
or EML account.

Todo:
    * Need to add event logging.
    * Need to add CLI interface.
    * Add YAML log file.
    * You need a main/API method - I think this is where to check if the account path exists.
    * Need to add arg that lets user select starting template file.
    * ReferencesAccount needs to be loadable via JSON file or another EAXS file or something ... 
"""

# import logging.
import jinja2
import logging
import os
import plac
import yaml
from .lib.account_object import AccountObject
from .lib.eaxs_maker import EAXSMaker
from .lib.addons import EAXSHelpers


class DarcMail():
    """ A class that creates EAXS files from Jinja2 templates and a source MBOX or EML account. """


    def __init__(self, account_args, eaxs_path, message_dir="messages", 
        attachment_dir="attachments", template_dir=None, charset="utf-8"):
        """ Sets instance attributes.
        
        Args:
            - account_args (dict): The account values to pass to lib.account_object.AccountObject().
            - eaxs_path (str): ???
            - template_dir (str): The path to a folder that contains Jinja2 template files. If None,
            this defaults to "eaxs_templates".
            - charset (str): The encoding to use for writing EAXS files.

        Attributes:
            - account (lib.account_object.AccountObject): ???
            - eaxs (lib.eaxs_maker.EAXSMaker): ???

        Example:
            ???
        """
        
        # set loggers; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.event_logger = logging.getLogger(__name__)
        self.event_logger.addHandler(logging.NullHandler())

        # set attributes
        self.account = AccountObject(**account_args)
        self.eaxs_path, self.eaxs_container = self._check_path(eaxs_path)
        self.message_dir = os.path.join(self.eaxs_container, message_dir)
        self.attachment_dir = os.path.join(self.eaxs_container, attachment_dir)
        self.charset = charset
        self.template_dir = template_dir if template_dir is not None else os.path.join(
            os.path.dirname(__file__), "eaxs_templates")

        # create an instance of EAXSMaker.
        self.eaxs = EAXSMaker(template_dir=self.template_dir, charset=self.charset, DarcMail=self,
        EAXSHelpers=EAXSHelpers)
        self.make_eaxs = lambda: self.eaxs.make(self.eaxs_path)


    def _check_path(self, filepath):
        """ ??? 
        
        Raises: ???
        """
        
        # ???
        filepath = os.path.abspath(filepath)
        if os.path.isfile(filepath):
            err = "DARCMAIL ERROR HERE???"
            self.logger.error(err)
            raise FileExistsError(err)

        # if needed, create the parent directory for @filepath.
        container = os.path.dirname(filepath)
        if container != "" and not os.path.isdir(container):
            self.logger.info("???")
            os.makedirs(container)
        
        return (filepath, container)


if __name__ == "__main__":
    pass
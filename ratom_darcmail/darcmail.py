#!/usr/bin/env python3

""" This module contains a class that creates EAXS files from Jinja2 templates and a source MBOX
or EML account.

Todo:
    * Need to add event logging.
    * Need to add CLI interface.
        - Accept References Account data?
    * Add YAML log file.
    * Work on docstrings: the first line is showing up as the module name.
        - This is somewhat related to Todo blocks in the docstrings.
    * Create test data to test single and multipart emails.
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


    def __init__(self, account_args, eaxs_path, template="Account.xml", template_dir=None,
        message_dir="messages", attachment_dir="attachments", charset="utf-8"):
        """ Sets instance attributes.
        
        Args:
            - account_args (dict): The values needed to create an instance of 
            lib.account_object.AccountObject().
            - eaxs_path (str): The filepath for the EAXS file to be written to.
            - template (str): The Jinja2 template to use. Note: this file must be present in
            @template_dir.
            - template_dir (str): The path to a folder that contains Jinja2 template files. If None,
            this defaults to "./eaxs_templates".
            - message_dir (str): The folder in which to write email messages as files.
            - attachment_dir (str): The folder in which to write email attachments as files.
            - charset (str): The encoding to use for writing EAXS, message, and attachment files.

        Attributes:
            - account (lib.account_object.AccountObject): The AccountObject associated with this
            DarcMail object, i.e. the email account data of interest.
            - eaxs_container (str): The containing folder for @eaxs_path.
            - eaxs (lib.eaxs_maker.EAXSMaker): This shouldn't need to be used unless you plan to 
            call the @eaxs.make() method from within your @template - i.e. render *another* Jinja2
            template from a call to @eaxs_make() from within @template.
            - make_eaxs (function): Use this to create the EAXS file at @eaxs_path.

        Example:
            >>> account_args = dict(path="tests/sample_files/eml", 
                    email_addresses="email@email.com")
            >>> drkml = DarcMail(account_args, "foo/foo.eaxs")
            >>> drkml.make_eaxs()
        """
        
        # set loggers; suppress logging by default.
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.event_logger = logging.getLogger(__name__)
        self.event_logger.addHandler(logging.NullHandler())

        # set attributes
        self.account = AccountObject(darcmail=self, **account_args)
        self.eaxs_path = os.path.abspath(eaxs_path)
        self.eaxs_container = os.path.dirname(self.eaxs_path)
        self.template = template
        self.template_dir = (template_dir if template_dir is not None else
            os.path.join(os.path.dirname(__file__), "eaxs_templates"))
        self.message_dir = os.path.join(self.eaxs_container, message_dir)
        self.attachment_dir = os.path.join(self.eaxs_container, attachment_dir)
        self.charset = charset
        
        # create an instance of EAXSMaker; create alias to its @make method.
        self.eaxs = EAXSMaker(template_dir=self.template_dir, charset=self.charset, DarcMail=self,
        EAXSHelpers=EAXSHelpers)
        self.make_eaxs = lambda: self.eaxs.make(eaxs_path=self.eaxs_path, template=self.template)


if __name__ == "__main__":
    pass
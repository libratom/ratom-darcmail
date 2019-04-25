#!/usr/bin/env python3

""" This module contains a class that creates EAXS files from Jinja2 templates and a source MBOX
or EML account.

Todo:
    * Need to add event logging.
    * Need to add CLI interface.
    * Add YAML log file.
    * You need a main/API method - I think this is where to check if the account path exists.
    * ReferencesAccount needs to be loadable via JSON file or something ... 
"""

# import logging.
import jinja2
import logging
import os
import plac
import yaml
from lib.account_object import AccountObject
from lib.eaxs_maker import EAXSMaker


class DarcMail():
    """ A class that creates EAXS files from Jinja2 templates and a source MBOX or EML account. """


    def __init__(self, account_args, template_dir=None, charset="utf-8"):
        """ Sets instance attributes.
        
        Args:
            - account_args (dict): The account values to pass to lib.account_object.AccountObject().
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
        self.charset = charset
        self.template_dir = template_dir if template_dir is not None else os.path.join(
            os.path.dirname(__file__), "eaxs_templates")

        # create an instance of EAXSMaker.
        self.eaxs = EAXSMaker(template_dir=self.template_dir, charset=self.charset)


if __name__ == "__main__":
    #pass

    # simple test ...
    logging.basicConfig(level=10)
    references_account = {"href": "ref_href_", "email_address": ["foo@ref.com", "bar@ref.com"], "ref_type": "SeeAlso"}
    account_args = dict(path="../tests/sample_files/eml",
                        email_address="email@email.com", is_eml=True,
                        global_id=None,
                        references_account=references_account)
    dm = DarcMail(account_args)
    dm.eaxs.make("TEST_EAXS.XML", DarcMailObject=dm)


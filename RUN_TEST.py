import logging, os
from ratom_darcmail.darcmail import DarcMail

# simple test ...
logging.basicConfig(level=10)
TEST_EAXS = "TEST_EAXS/TEST_EAXS.XML"


references_account = {"href": "ref_href_", "email_address": ["foo@ref.com", "bar@ref.com"], "ref_type": "SeeAlso"}
account_args = dict(path="tests/sample_files/eml",
                    email_addresses="email@email.com", is_eml=True,
                    global_id=None,
                    references_account=references_account)
dm = DarcMail(account_args, TEST_EAXS)
dm.eaxs.make(dm.eaxs_path)

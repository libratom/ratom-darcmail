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
dm_eml = DarcMail(account_args, TEST_EAXS)
#dm_eml.eaxs.make(dm_eml.eaxs_path)
#dm_eml.make_eaxs() # shorter way of doing the line above.
fol = next(dm_eml.account.get_folders())
msg = next(fol.get_messages())
#dm_eml.account == fol.account == msg.folder.account # True
def _fail(): raise Exception("hell")
msg.email.fail = _fail # should update parse_errors.

#mbox_args = account_args
#mbox_args["path"] = mbox_args["path"].replace("eml", "mbox")
#mbox_args["is_eml"] = False
#dm_mbox = DarcMail(mbox_args, TEST_EAXS)
#dm_mbox.make_eaxs()

import logging, os
from ratom_darcmail.darcmail import DarcMail

# simple test ...
logging.basicConfig(level=10)
TEST_EAXS = "TEST_EAXS_/TEST_EAXS.XML"


references_account = {"href": "ref_href_", "email_address": ["foo@ref.com", "bar@ref.com"], "ref_type": "SeeAlso"}
account_args = dict(path="../sample_files/mbox",
                    email_addresses="email@email.com", is_eml=False,
                    global_id=None,
                    references_account=references_account)
dm = DarcMail(account_args, TEST_EAXS)
##dm.eaxs.make(dm.eaxs_path)
##dm.make_eaxs() # shorter way of doing the line above.
fol = next(dm.account.get_folders())
msg = next(fol.get_messages())
##dm.account == fol.account == msg.folder.account # True
##def _fail(): raise Exception("hell")
##msg.email.fail = _fail # should update parse_errors.
for p in msg.get_submessages():
    print(p.mock_path, p.write_path, sep="\t|\t")

##mbox_args = account_args
##mbox_args["path"] = mbox_args["path"].replace("eml", "mbox")
##mbox_args["is_eml"] = False
##dm_mbox = DarcMail(mbox_args, TEST_EAXS)
##dm_mbox.make_eaxs()

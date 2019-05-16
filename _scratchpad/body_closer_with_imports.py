import sys
sys.path.append("../")
from ratom_darcmail.lib.addons import EAXSHelpers
from ratom_darcmail.darcmail import DarcMail

account_args = dict(path="../tests/sample_files/eml",
                    email_addresses="email@email.com", is_eml=True,
                    global_id=None)
dm = DarcMail(account_args, "")

fol = next(dm.account.get_folders())
msg = next(fol.get_messages())
parts = msg.get_submessages()


opened_parts = []
for part in parts:
        for closed_part in EAXSHelpers["close_folders"](part, opened_parts,
            "mock_path"):
            print("close:", closed_part.mock_path)
        print("open:", part.mock_path)
print("\n*** close leftovers\n")
for opened_part in reversed(opened_parts):
        print("close:", opened_part.mock_path)

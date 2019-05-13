#!/usr/bin/env python3

"""
Prefer native data structures (dicts, etc.) over custom classes.
At least class attributes should be native types.
That's why it's ok to have @nitin.{attribute} but not @nitin.{attribute}.{subattribute}, etc.
"""


##### currently NOT implemented; should be contra-indicated (too complex, volatile)
class ReferencesAccount():
    def __init__(self, references_account):
        self.references_account = references_account # after sanitizing.
        self._reference_types = ["PreviousContent", "SubsequentContent", "Supplemental", 
            "SeeAlso", "SeeInstead"]
        pass

nitin_refs = [{"href":"FOO", "email_address":["nitaro74@gmail.com"], "reftype":"SeeAlso"}
    ] # list of dicts; @reftype must be in @self._reference_types; @email_address can be None.
    # TODO: error on illegal keys.


#####
class Account():
    def __init__(self, account_dir, email_address, is_eml, global_id, references_account=None, 
        **kwargs):
        pass

nitin_account = Account(account_dir="/nitin", email_address=["nitaro74@gmail.com"], is_eml=False, 
    global_id=None, references_account=ReferencesAccount(nitin_refs))

## user attributes.
# nitin.account_dir # str. NORMALIZED.
# nitin.is_eml # False
# nitin.email_address # = ["nitaro74@gmail.com"]
# nitin.global_id # auto-assigned if None
# nitin.references_account # must be a ReferencesAccount instance

## computed attributes.
# nitin.folders # generator object; each item has a message tuple: 
    # folder "name", relpath" (normalized), "mbox" object, "messages" object
    # Note: "folders" is NOT recursive because messages will be first class citizens.
    # nitin.folders[0].name # base folder name.
    # nitin.folders[0].relpath # normalized relative path to @self.account_dir, use for <Message/RelPath.
    # nitin.folders[0].messages # yields email.message.Message objects.
    # nitin.folders[0].mbox # None if @self.is_eml else dict: 
        # {"rel_path": "", "eol": "", "hash_value": "", "hash_function": ""}
            # @eol must be in ["CR", "LF", "CRLF"]
            # @hash_function is None if @hash_value is None else must be in:
            # ["MD5", "WHIRLPOOL", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512", "RIPEMD160"]
            # Note: Omit a hash function and document and example of how to import 
            # tomes_packager.lib.file_object through @self.kwargs and use it with a Jinja template.
        # Note: I'd omit @mbox since it's not required and having a METS manifest is a better way to
        # do it. Especially because EAXS wasn't designed for EML, it's silly to only have it store
        # hashed for MBOX sources.


class Message(email.message.Message):
    def __init__(self):
        self["Local-Id"] = # incrementer.





# TODO: can you get rid of .folders and just put all that data in .messages.message?
# Should be possible because the generator will still organize output by each folder.



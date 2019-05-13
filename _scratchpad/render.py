import logging
import jinja2

"""
Todo:
    * Remove blank lines from template before rendering.
"""

### TODO: MOVE!!!
def to_close(folder, opened):

    closing = []
    
    if len(opened) != 0:
        for op in reversed(opened):
            if not folder.path.startswith(op.path):
                closing.append(op)
                opened.remove(op)
    
    opened.append(folder)

    return closing


class EAXSMaker():


    def __init__(self, darcmail_obj=None, charset="utf-8", *args, **kwaegs):
        

        # You need a pre-written set of test/sample object data.
        account = type("DarcMail", (), {}) #TODO: pass in.
        account.email_address = ["foo@foo.com", "bar@bar.com"]
        account.global_id = "123"
        account.is_eml = False
        account.references_account = {"href": "references account HREF", "email_address": ["foo1@foo.com"], "ref_type": "SeeAlso"}

        # TODO: pass in. 
        folder1 = type("Folder", (), {})
        folder1.name = "a"
        folder1.path = "a"
        folder1.mbox = type("Mbox", (), {})
        folder1.mbox.relpath = "a/1.mbox"
        folder1.mbox.eol = "CR"
        folder2 = type("Folder", (), {})
        folder2.name = "b"
        folder2.path = "a/b"
        folder2.mbox = type("Mbox", (), {})
        folder2.mbox.relpath = "a/b/1.mbox"
        folder2.mbox.eol = "LF"
        folder3 = type("Folder", (), {})
        folder3.name = "c"
        folder3.path = "c"
        folder3.mbox = type("Mbox", (), {})
        folder3.mbox.relpath = "c/1.mbox"
        folder3.mbox.eol = "CRLF"
        account.folders = [folder1, folder2, folder3]

        self.to_close = to_close #TODO:

        # ???
        self.logger = logging.getLogger(__name__)

        # ???
        self.account = account
        self.charset = charset


    def make(self, *args, **kwargs):

        env = jinja2.Environment(loader=jinja2.FileSystemLoader("."),  trim_blocks=True, lstrip_blocks=True,
                comment_start_string="<!--#", comment_end_string="#-->")
        #with open("account.xml", encoding=self.charset) as tf:
        #        eaxs_template = tf.read()
            
        # create the Jinja renderer.
        try:
            template = env.get_template("account.xml")
        except jinja2.exceptions.TemplateSyntaxError as err:
            raise ValueError(err)
        
        try:
            eaxs = template.stream(EAXS_OBJECT=self, *args, **kwargs)
            with open("TEST.XML", "w", encoding=self.charset, 
                    errors="xmlcharrefreplace") as f:
                i = 0
                for line in eaxs:
                    if line.strip() == "":
                        continue
                    f.write(line)
                    if (i + 1) % 100 == 0:
                        self.logger.info("Current write operation: {}".format(i))
                    i += 1
        except (AttributeError, TypeError, jinja2.exceptions.UndefinedError) as err:
            raise ValueError(err)

        return

if __name__ == "__main__":
    #pass
    em = EAXSMaker()
    em.make()

import email
import email.policy

with open("../tests/sample_files/eml/inbox/1_.eml", "rb") as eml:
    mess = email.message_from_binary_file(eml, policy=email.policy.Compat32())

### Look familiar? This is the folder closer with different var names!
### So it can be re-used.
def close_parts(part, opened_parts):

    parts_to_close = []
    for opened in reversed(opened_parts):  
        if not part.path.startswith(opened.path):
            parts_to_close.append(opened)
            opened_parts.remove(opened)    
    opened_parts.append(part)
    return parts_to_close

###
class Body():
        def __init__(self, msg, path):
                self.msg = msg
                self.path = path

###
parts = []
def split_msg(msg, path="inbox"):
        
        ctype = msg.get_content_type().replace("/", "_")
        path += "/{}_{}".format(ctype, len(parts))

        part = Body(msg, path)
        parts.append(part)
        if msg.is_multipart():
                for p in msg._payload:
                        split_msg(p, path)
                
        return

split_msg(mess)

###
opened_parts = []
for part in parts:
        for closed_part in close_parts(part, opened_parts):
                print("close:", closed_part.path)
        print("open:", part.path)
print("\n*** close leftovers\n")
for opened_part in reversed(opened_parts):
        print("close:", opened_part.path)

from lxml import etree

folders = ['a', 'a/b', 'a/b/c', 'a/d', 'a/d/e', 'a/f']
folders = ['a', 'a/b', 'a/b/c', 'd', 'd/e', 'f']

###
def to_close(folder, opened):

    closing = []
    
    if len(opened) != 0:
        for op in reversed(opened):
            if not folder.startswith(op):
                closing.append(op)
                opened.remove(op)
    
    opened.append(folder)

    return closing

###
opened = []
for folder in folders:

    closing = to_close(folder, opened)

    for f in closing:
        print("Closed: ", f)
    print("Opened: ", folder)

for f in reversed(opened):
    print("Closed", f)



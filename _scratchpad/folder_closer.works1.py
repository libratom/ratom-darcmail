from lxml import etree

folders = ['a', 'a/b', 'a/b/c', 'a/d', 'a/d/e', 'a/f']
#folders = ['a', 'a/b', 'a/b/c', 'd', 'd/e', 'f']

opened = []

for folder in folders:
    
    if len(opened) != 0:
        for op in reversed(opened):
            if not folder.startswith(op):
                print("closed: ", op)
                opened.remove(op)

    print("opened: ", folder)
    opened.append(folder)

print("__")
for op in reversed(opened):
    print("closed: ", op)


import pdb
print "hello world"
foo = "bar"
baz = "bonk"
i=0
list_of_lists = [ [1, 2, 3], [4, 5, 6], [7, 8, 9]]
pdb.set_trace()
for list in list_of_lists:
    for x in list:
        print x

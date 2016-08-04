#!/usr/bin/python

import sys


class Node:
  def __init__(self):
      self.parent = None
      self.childs = []  # list of ids
      self.defined = 0

tree = {}

for line in sys.stdin:
    s_id, p_id = [ int(x) for x in line.split('\t') ]

    # taxo[s_id] = p_id
    if s_id == p_id:
        print "ERR s_id == p_id", s_id
        continue

    # check current rec
    node = Node()
    if s_id in tree:
        node = tree[s_id]
    if node.defined:
        print "ERR fact.defined", s_id
    node.defined = 1
    node.parent = p_id
    tree[s_id] = node

    # check parent
    node = Node()
    if p_id in tree:
        node = tree[p_id]
    # print "tree[", p_id,"].childs : ", node.childs, "+=", s_id
    node.childs.append(s_id)
    tree[p_id] = node

# find root
root = tree.keys()[0];
while tree[root].parent in tree:
    root = tree[root].parent

maxlevel = 0
childs = {}
sum_accessed = 0

def descend(id, level, access):
    # print "descend", id, taxo[id].childs
    global maxlevel
    global childs
    global sum_accessed

    if level > maxlevel:
        maxlevel = level
    node = tree[id]
    if 0 == node.defined:
        print "ERR: not defined ", id
        access = False
    nchilds = len(node.childs)
    childs[nchilds] = 1 if nchilds not in childs else childs[nchilds] + 1
    for ch in node.childs:
        if ch in tree:
          if access:
            sum_accessed += 1
          descend(ch, level + 1, access)


tree[root].defined = 1
descend(root, 0, True)

tree[root].defined = 0
sum_defined = sum([x.defined for x in tree.values()])

print "tree elements defined: ", sum_defined
print "elements accessible from root: ", sum_accessed

if sum_accessed != sum_defined:
    print "ERR: full tree size:", sum_defined, " accessible from the root:", sum_accessed

print "root: ", root #, taxo['20072770'].childs
print "depth: ", maxlevel
print "leafs: ", 0 if 0 not in childs else childs[0]
print "nof childs distribution: ", childs

# import pprint
# pprint.pprint(childs)

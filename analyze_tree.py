#!/usr/bin/python

import sys


class Node:
  def __init__(self):
      self.parent = None
      self.childs = []  # list of ids
      self.defined = False

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
    node.defined = True
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

def descend(id, level):
    # print "descend", id, taxo[id].childs
    global maxlevel
    global childs
    if level > maxlevel:
        maxlevel = level
    node = tree[id]
    if not node.defined:
        print "ERR: not defined ", id

    nchilds = len(node.childs)
    childs[nchilds] = 1 if nchilds not in childs else childs[nchilds] + 1
    for ch in node.childs:
        descend(ch, level + 1)


descend(root, 0)
print "root: ", root #, taxo['20072770'].childs
print "depth: ", maxlevel
print "leafs: ", 0 if 0 not in childs else childs[0]
print "nof childs distribution: ", childs
# import pprint
# pprint.pprint(childs)

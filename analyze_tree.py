#!/usr/bin/python

import sys


class Node:
  def __init__(self, id):
      self.id = id
      self.parent = None
      self.childs = []  # list of ids
      self.defined = 0
      self.accessed = 0

tree = {}
def loadTree():
    global tree
    for line in sys.stdin:
        s_id, p_id, meta = line.strip().split('\t')

        # taxo[s_id] = p_id
        if s_id == p_id:
            print "ERR s_id == p_id", s_id
            continue

        # check current rec
        node = Node(s_id)
        if s_id in tree:
            node = tree[s_id]
        if node.defined:
            print "ERR fact.defined", s_id
        node.defined = 1
        node.parent = p_id
        node.meta = meta
        tree[s_id] = node

        # check parent
        node = Node(p_id)
        if p_id in tree:
            node = tree[p_id]
        # print "tree[", p_id,"].childs : ", node.childs, "+=", s_id
        node.childs.append(s_id)
        tree[p_id] = node

loadTree()

def findRoot(tree):
    root = tree.values()[0];
    while root.parent in tree:
        root = tree[root.parent]
    return root


root = findRoot(tree)
childs = {}

def dft(id, level, accessible):
    global childs
    node = tree[id]
    if 0 == node.defined:
        print "ERR: not defined ", id
        accessible = False
    node.accessed = 1 if accessible else 0
    nchilds = len(node.childs)
    childs[nchilds] = 1 if nchilds not in childs else childs[nchilds] + 1
    return level if len(node.childs) == 0 else max([dft(ch, level + 1, accessible) for ch in node.childs])


def printStats():
    maxlevel = max([ dft(x, 1, True) for x in root.childs ])
    sum_defined = sum([x.defined for x in tree.values()])
    sum_accessed = sum([x.accessed for x in tree.values()])
    print "tree elements defined: ", sum_defined
    print "elements accessible from root: ", sum_accessed
    if sum_accessed != sum_defined:
        print "ERR: full tree size:", sum_defined, " accessible from the root:", sum_accessed
    print "root: ", root.id #, taxo['20072770'].childs
    print "depth: ", maxlevel
    print "leafs: ", 0 if 0 not in childs else childs[0]
    print "nof childs distribution: ", childs


def bft(actlevel, level, function):
    nextlevel = []
    for node in actlevel:
        childs = [ tree[x] for x in node.childs ]
        nextlevel = nextlevel + childs
        for ch in childs:
            function(ch)
    return 0 if 0 == len(nextlevel) else bft(nextlevel, level + 1, function)

def printNode(node):
    print node.id, node.parent, node.meta

if function == __main__:
    if len(sys.argv) == 1 and sys.argv[0] == 'print'
        bft([root], 0, printNode)
    else
        printStats

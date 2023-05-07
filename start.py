#!/bin/env python

import re
import os


from symboltree import SymbolTree
from objtree import ObjTree
from dot import Dot

# For debug only
import pprint
pp = pprint.PrettyPrinter(indent=4)




def main():
    print("Started\n")
    st = SymbolTree("/home/nevada/crane/screw/build/9daaa12_ru_ru_2560_e1_b140")
    ot = ObjTree(st.objects)
    d = Dot()
    d.node_args = "shape=egg, color=red"
    d.vertex_args = "color=green"

    d.GraphEnter("digraph")
    ot.GetDotNotation(d)
    d.GraphExit()

    # s = "digraph {\n"
    # s += ot.GetDotNotation()
    # s += "}"
    # print(s)
    #
    # f = open("test.dot", "w+")
    # f.write(s)
    # f.close()
    # d.GraphAddArg("// Start of graph")
    # d.AddNode("NODE1")
    # d.AddNode("NODE2")
    # d.SubgraphEnter("cluster_temp")
    # d.AddNode("NODE2x")
    # d.AddVertex("NODE1", "NODE2")
    # d.AddVertex("NODE2", "NODE3", "label=11")
    # d.node_args = ""
    # d.AddVertex("NODE1", "NODE2")
    # d.AddVertex("NODE2", "NODE3", "label=11")
    # d.SubgraphEnter("cluster_temp")
    # d.SubgraphEnter("cluster_temp")
    # d.SubgraphEnter("cluster_temp")
    # d.SubgraphEnter("cluster_temp")
    # d.AddNode("NODE3x")
    d.Print()
    d.FileWrite("test.dot")
    stream = os.popen('bash -c "dot -Tpng test.dot > test.png"')




if __name__ == '__main__':
    main()
else:
    print("Refused to start")
    exit(1)

#!/bin/env python

import re
import os


from symboltree import SymbolTree
from objtree import ObjTree
from dot import Dot

# For debug only
import pprint
pp = pprint.PrettyPrinter(indent=4)



st = []

# def main():
print("Started\n")
# st = SymbolTree("/home/nevada/crane/screw/build/9daaa12_ru_ru_2560_e1_b140")
st = SymbolTree("/home/nevada/crane/screw/build/9daaa12_ru_ru_2560_e1_b140/pos")
ot = ObjTree(st.objects)
d = Dot()
d.node_args = "color=black, shape=oval"
d.subgraph_colors = ['#D0D0FF', '#D0FFD0', '#FFD0D0', '#FFFFA0', '#FFA0FF', '#A0FFFF']
d.SubgraphAddArg("style=filled")

d.digraph = True
d.GraphEnter()
ot.GetDotNotation(d)

vertexes = {}
varss = {}

def AddIfMissing(dictX, arg, val):
    if arg not in dictX:
        dictX[arg] = val

def AddVertex(nodeA, nodeB, fun):
    vertex_name = "%s->%s" % (nodeA, nodeB)
    AddIfMissing(vertexes, vertex_name, {'nodeA': nodeA, 'nodeB': nodeB, 'calls': []})
    vertexes[vertex_name]['calls'].append(fun)

def AddVar(nodeA, nodeB, fun):
    if nodeA > nodeB:
        b,a = nodeA, nodeB
    else:
        a,b = nodeA, nodeB
    vertex_name = "%s--%s" % (a, b)
    AddIfMissing(varss, vertex_name, {'nodeA': a, 'nodeB': b, 'calls': []})
    varss[vertex_name]['calls'].append(fun)

f = open("function_calls.csv", "w+")
f.write('Definition,Function,Caller\n')

for fun_def in st.globalFunctions:
    fun_name = fun_def.symbol
    fun_loc = fun_def.loc['fullobj']
    usages = [s.loc for s in st.allUndefs if s == fun_name and s.loc['fullobj'] != fun_loc]
    if usages:
        for usageN in usages:
            AddVertex(usageN['fullobj'], fun_def.loc['fullobj'], fun_name)
            f.write('"%s",%s,"%s"\n' % (fun_def.loc['relpath'], fun_name, usageN['relpath']))
f.close()

f = open("vars.csv", "w+")
f.write('Definition,Variable,Caller\n')

for variable_def in st.globalVars:
    pp.pprint(variable_def)
    var_name = variable_def.symbol
    fun_loc = variable_def.loc['fullobj']
    usages = [s.loc for s in st.allUndefs if s == var_name and s.loc['fullobj'] != fun_loc]
    if usages:
        for usageN in usages:
            AddVar(usageN['fullobj'], variable_def.loc['fullobj'], var_name)
            f.write('"%s",%s,"%s"\n' % (variable_def.loc['relpath'], var_name, usageN['relpath']))
f.close()


d.SubgraphEnter("function_calls")
d.vertex_args = ""
for v in vertexes:
    vx = vertexes[v]
    cmt = "color=red,penwidth=3" if (len(vx['calls']) > 1) else "constraint=false,color=black"
    cmt += ",weight=%d" % (len(vx['calls']))
    d.AddVertex(vx['nodeA'], vx['nodeB'], cmt)
d.SubgraphExit()


d.SubgraphEnter("variables")
d.vertex_args = "constraint=false,dir=none,color=blue"
for v in varss:
    vx = varss[v]
    cmt = "penwidth=2" if (len(vx['calls']) > 1) else "penwidth=1"
    cmt += ",weight=%d" % (3*len(vx['calls']))
    d.AddVertex(vx['nodeA'], vx['nodeB'])
d.SubgraphExit()


d.GraphExit()
d.Print()
d.FileWrite("test.dot")
# stream = os.popen('bash -c "dot -Tpng test.dot > test.png"')



#
# if __name__ == '__main__':
#     main()
# else:
    # print("Refused to start")
    # exit(1)

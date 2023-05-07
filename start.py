#!/bin/env python

import re

from symboltree import SymbolTree
from objtree import ObjTree

# For debug only
import pprint
pp = pprint.PrettyPrinter(indent=4)




def main():
    print("Started\n")
    st = SymbolTree("/home/nevada/crane/screw/build/9daaa12_ru_ru_2560_e1_b140")

    ot = ObjTree(st.objects)
    s = ot.GetDotNotation()
    # print(ot.dirs)
    # pp.pprint(ot.subdirs)


    dirs = []

    # for path,obj in [(o['relloc'],o['objname']) for o in st.objects]:
        # print(path,obj)


    # for i in st.globalFunctions:
    #     print(i)
    #
    #
    # for i in Undefs:
    #     if i.symbol not in [f.symbol for f in GlobalFunctions]:
    #         print(i)







if __name__ == '__main__':
    main()
else:
    print("Refused to start")
    exit(1)

#!/bin/env python

import os
import re

# For debug only
import pprint
pp = pprint.PrettyPrinter(indent=4)

print("Started\n")

class SymbolFlags:
    def __init__(self, flags, section):
        self.str = flags
        if len(flags) != 7:
            raise ValueError("Bad flags length")

        self.isGlobal = (self.str[0] in "gu!")
        self.isGlobalUniq = (self.str[0] in "u")
        self.isLocal = (self.str[0] in "l!")

        self.isWeak = (self.str[1] in "w")

        self.isCtor = (self.str[2] in "C")

        self.isWarning = (self.str[3] in "W")

        self.isIndirect = (self.str[4] in "I")
        self.isRelocator = (self.str[4] in "i")

        self.isDebug = (self.str[5] in "d")
        self.isDynamic = (self.str[5] in "D")
        self.isStatic = (self.str[5] in " ")

        self.isFunction = (self.str[6] in "F")
        self.isFile = (self.str[6] in "f")
        self.isObject = (self.str[6] in "O")

        self.isAbs = section == "*ABS*"
        self.isCom = section == "*COM*"
        self.isUnd = section == "*UND*"

    def __str__(self):
        return self.str.replace(" ", "")

class HexStr:
    def __init__(self, hex):
        self.hex = hex
    def __str__(self):
        return self.hex
    def __int__(self):
        return int(self.hex, 16)

class Symbol:
    rex = re.compile(r"^([0-9A-Fa-f]+)[ \t](.......)[ \t]+([^ \t]+)[ \t]+([^ \t]*)[ \t]+([^ \t]*)$")
    sectionfilter = re.compile(r"^(\.?[^ \.]+)(\..+)?")
    def __init__(self, line, loc):
        m = re.search(self.rex, line)
        if not m:
            raise ValueError("RE does not match")

        self.loc = loc
        self.addr = HexStr(m.group(1))
        self.flagsstr = m.group(2)
        self.fullsection = m.group(3)
        self.segsize = HexStr(m.group(4))
        self.symbol   = m.group(5)

        self.section  = self.GetSectionHead()
        self.flags    = SymbolFlags(self.flagsstr, self.section)

    def GetSectionHead(self):
        m = re.search(self.sectionfilter, self.fullsection)
        if not m:
            return self.fullsection
        if m.group(1) == "":
            return self.fullsection
        return m.group(1)

def read_dump(command, arr, loc):
    stream = os.popen(command)
    for line in stream:
        line = line.replace("\r", "").replace("\n", "")
        try:
            ms = Symbol(line, loc)
        except ValueError:
            continue
        arr.append(ms)

def GetObjectsInPath(path):
    base = os.path.normpath(path)
    results = [];
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames]:
            if not filename.endswith(".o"):
                continue
            fpath = dirpath + "/" + filename
            rpath = os.path.relpath(fpath, base)
            rloc = os.path.relpath(dirpath, base)
            objname = re.sub(" ", "_", rpath)
            objname = re.sub(r"^(\.\/)(.*)$", r"\2", objname)
            objname = re.sub(r"\.[^\.]*$", "", objname)
            objname = re.sub(r"/", "_", objname)
            if not rloc.startswith('.'):
                rloc = "./" + rloc
            loc = {
                'filename': filename,
                'objname': objname,
                'relpath': rpath,
                'relloc': rloc,
                'fullpath': fpath
            }
            results.append(loc)
    pp.pprint(results)
    return results

def DumpFilefInLocations(locations):
    arr = []
    for loc in locations:
        read_dump("objdump -t %s" % loc['fullpath'], arr, loc)
    return arr

# read_dump("objdump -t socket.o")
loc = GetObjectsInPath("/home/nevada/crane/screw/build/9daaa12_ru_ru_2560_e1_b140")
arr = DumpFilefInLocations(loc)
for item in [i for i in arr if i.flags.isFunction]:
    print(item.loc['objname'], item.symbol)

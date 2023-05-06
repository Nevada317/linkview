#!/bin/env python

import os
import re

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
    def __init__(self, line):
        m = re.search(self.rex, line)
        if not m:
            raise ValueError("RE does not match")

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

def read_dump(command):
    stream = os.popen(command)
    for line in stream:
        line = line.replace("\r", "").replace("\n", "")
        try:
            ms = Symbol(line)
        except ValueError:
            continue

        if ms.flags.isFunction:
            continue
        if int(ms.segsize) == 0:
            continue

        print("")

        for tag in ms.__dict__.items():
            print("%s\t- %s" %(tag[0], tag[1]))

        #m = ms.m
        #for i in range(0, len(m.groups())+1):
        #    e = m.group(i)
        #    print("m[%d] = %s" % (i, e))
        #line = line.replace(" ", ".").replace("\t", ":")
        print("< %s >" % line)

read_dump("objdump -t socket.o")




import re

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
        self.symbol = m.group(5)

        self.line = line

        self.section  = self.GetSectionHead()
        self.flags    = SymbolFlags(self.flagsstr, self.section)

    def GetSectionHead(self):
        m = re.search(self.sectionfilter, self.fullsection)
        if not m:
            return self.fullsection
        if m.group(1) == "":
            return self.fullsection
        return m.group(1)

    def __str__(self):
        return "@%s \t%s \t%s \t%s \t@%s \ts%d\n%s" % (self.addr, self.section, self.flags, self.symbol, self.loc['objname'], self.segsize, self.line)

import os
import re

from symbol import Symbol

class SymbolTree:
    def __init__(self, path):
        self.objects = []
        self.symbols = []
        self.FillObjects(path)
        self.FinalSplit()

    def FillObjects(self,path):
        base = os.path.normpath(path)
        results = [];
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in [f for f in filenames]:
                if not filename.endswith(".o"):
                    continue
                fpath = dirpath + "/" + filename
                rpath = os.path.relpath(fpath, base)
                rloc = os.path.relpath(dirpath, base)
                fobjname = re.sub(" ", "_", rpath)
                fobjname = re.sub(r"^(\.\/)(.*)$", r"\2", fobjname)
                fobjname = re.sub(r"\.[^\.]*$", "", fobjname)
                fobjname = re.sub(r"/", "_", fobjname)

                sobjname = re.sub(" ", "_", filename)
                sobjname = re.sub(r"^(\.\/)(.*)$", r"\2", sobjname)
                sobjname = re.sub(r"\.[^\.]*$", "", sobjname)
                sobjname = re.sub(r"/", "_", sobjname)
                if not rloc.startswith('.'):
                    rloc = "./" + rloc
                loc = {
                    'filename': filename,
                    'fullobj': fobjname,
                    'objname': sobjname,
                    'relpath': rpath,
                    'relloc': rloc,
                    'fullpath': fpath
                }
                self.AppendObject(loc)

    def AppendObject(self, obj):
        self.objects.append(obj)
        stream = os.popen("objdump -t %s" % obj['fullpath'])
        for line in stream:
            line = line.replace("\r", "").replace("\n", "")
            try:
                ms = Symbol(line, obj)
            except ValueError:
                continue
            self.symbols.append(ms)

    def FinalSplit(self):
        self.globalVars = [s for s in self.symbols if (s.flags.isGlobal and s.flags.isObject and not s.flags.isUnd)]
        self.globalFunctions = [s for s in self.symbols if (s.flags.isGlobal and s.flags.isFunction and not s.flags.isUnd)]
        self.allUndefs = [s for s in self.symbols if (s.flags.isUnd)]
        self.absolutes = [s for s in self.symbols if (s.flags.isAbs)]


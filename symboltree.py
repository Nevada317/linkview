import os
import re

from symbol import Symbol

class SymbolTree:
    def __init__(self):
        self.objects = []
        self.symbols = []
        pass

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




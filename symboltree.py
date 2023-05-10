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
        self.FillFunctionCalls()
        self.FillVariables()


    def FillFunctionCalls(self):
        self.functionCalls = {}
        for fun_def in self.globalFunctions:
            fun_name = fun_def.symbol
            usages = [s for s in self.allUndefs if s == fun_name]
            if usages:
                if not fun_name in self.functionCalls:
                    self.functionCalls[fun_name] = []
                for usageN in usages:
                    self.functionCalls[fun_name].append(usageN)

    def FillVariables(self):
        self.crossVars = {}
        for var_def in self.globalVars:
            var_name = var_def.symbol
            usages = [s for s in self.allUndefs if s == var_name]
            if usages:
                if not var_name in self.crossVars:
                    self.crossVars[var_name] = []
                for usageN in usages:
                    self.crossVars[var_name].append(usageN)



#################################### PRIVATES

    def _AddIfMissing(self, dictX, arg, val):
        if arg not in dictX:
            dictX[arg] = val

    def _AddVertex(self, filleddict, nodeA, nodeB, fun):
        vertex_name = "%s->%s" % (nodeA, nodeB)
        self._AddIfMissing(filleddict, vertex_name, {'nodeA': nodeA, 'nodeB': nodeB, 'calls': []})
        filleddict[vertex_name]['calls'].append(fun)

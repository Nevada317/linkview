

class ObjTree:
	def __init__(self, objs):
		self.objects = objs
		self.dirs = []
		self.subdirs = {}
		for obj in self.objects:
			path = obj['relloc']
			self.AddDir(path)
		self.dirs.sort()

	def AddDirRecursive(self, dirpath):
		if dirpath in self.dirs:
			return
		offset = 0
		while (loc := dirpath.find("/", offset)) >= 0:
			self.AddDir(dirpath[:loc])
			offset = loc + 1
		self.AddDir(dirpath)
		self.subdirs[parent] = subdirs

	def AddDir(self, dirpath):
		if dirpath in self.dirs:
			return
		self.dirs.append(dirpath)
		n = dirpath.rfind("/")
		if n > 0:
			parent = dirpath[:n]
			subdirs = self.subdirs.get(parent, [])
			if dirpath not in subdirs:
				subdirs.append(dirpath)
				self.subdirs[parent] = subdirs

	def GetDotNotation(self):
		self.dot_indent = 1
		self.dot_indent_char = '\t'
		self.dot_str = ""
		self.DotSubdir('.')
		return self.dot_str

	def DotSubdir(self, path):
		print("Entering %s" % (path))
		if path != '.':
			self.Dot_AddDir(path)
		for obj in [obj for obj in self.objects if obj['relloc'] == path]:
			print("  Obj %s" % (obj['objname']))
			self.Dot_AddObject(obj)
		subdirs = self.subdirs.get(path, [])
		for sd in subdirs:
			self.DotSubdir(sd)
		print("Ending %s" % (path))
		if path != '.':
			self.Dot_EndDir()

	def Dot_AddDir(self, name):
		dirname = name.replace("./", "").replace("/", "_")
		ind = self.dot_indent_char * self.dot_indent
		self.dot_str += "%ssubgraph cluster_%s {\n" % (
			ind,
			dirname
			)
		self.dot_indent += 1
		ind = self.dot_indent_char * self.dot_indent
		self.dot_str += "%s// Dir: %s\n" % (
			ind,
			name
			)
		pass

	def Dot_EndDir(self):
		self.dot_indent -= 1
		ind = self.dot_indent_char * self.dot_indent
		self.dot_str += "%s}\n" % (
			ind
			)
		pass


	def Dot_AddObject(self, obj):
		ind = self.dot_indent_char * self.dot_indent
		self.dot_str += "%s%s [label=\"%s\"];\n" % (
			ind,
			obj['fullobj'],
			obj['objname']
			)
		pass






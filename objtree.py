

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

	def GetDotNotation(self, dot):
		self.dot = dot
		self.DotSubdir('.')
		self.dot = 0

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
		if not self.dot:
			return
		dirname = name.replace("./", "").replace("/", "_")
		subdirname = name.split("/")[-1]
		self.dot.SubgraphEnter("cluster_" + dirname)
		self.dot.AddComment("Dir: %s" % name)
		self.dot.AddCustomLine('label="%s"' % subdirname)

	def Dot_EndDir(self):
		if not self.dot:
			return
		self.dot.SubgraphExit()

	def Dot_AddObject(self, obj):
		if not self.dot:
			return
		self.dot.AddNode(obj['fullobj'], 'label="%s"' % obj['objname'])






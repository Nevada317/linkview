

class ObjTree:
	def __init__(self, objs):
		self.objects = objs
		self.dirs = []
		self.subdirs = {}
		for obj in self.objects:
			path = obj['relloc']
			self.AddDir(path)
		self.dirs.sort()
		print("#####")
		print(self.dirs)

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
		s = self.DotSubdir('.')

	def DotSubdir(self, path):
		print("Entering %s" % (path))
		for obj in [obj for obj in self.objects if obj['relloc'] == path]:
			print("  Obj %s" % (obj['objname']))
		subdirs = self.subdirs.get(path, [])
		for sd in subdirs:
			self.DotSubdir(sd)
		print("Ending %s" % (path))






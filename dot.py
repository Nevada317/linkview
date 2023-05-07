import os

class Dot:
	def __init__(self):
		self.indent_char = "\t"
		self.subgraph_colors = ['red', 'green', 'blue', 'cyan']
		self.node_args = ""
		self.vertex_args = ""
		self.digraph = False

		self._string = ""
		self._opened = False
		self._f = 0
		self._indent = 0
		self._graph_args = []
		self._subgraph_args = []
		self._subgraph_color_index = 0
		self._subgraph_depth = 0
		pass

	def _Sync(self):
		if self._opened:
			self._f.write(self._string)
			self._string = ""

	def _AddLine(self, line):
		self._indent -= line.count("}")
		self._string += self.indent_char * self._indent
		self._string += line
		self._string += '\n'
		self._indent += line.count("{")
		self._Sync()

	def Print(self):
		print(self._string)

	def FileWrite(self, filename):
		self.FileOpen(filename)
		self.FileClose()

	def FileOpen(self, filename):
		if self._opened:
			return
		self._f = open(filename, "w+")
		self._opened = True
		self._Sync()

	def FileClose(self):
		if not self._opened:
			return
		self._Sync()
		self._f.close()
		self._opened = False

# ###########################################

	def AddNode(self, node, args=""):
		line = node
		args_line = args
		if args_line and self.node_args:
			args_line += ", "
		if self.node_args:
			args_line += self.node_args
		if args_line:
			line += " [%s]" % args_line
		self._AddLine(line + ";")

	def AddVertex(self, nodeA, nodeB, args=""):
		if self.digraph:
			line = "%s -> %s" % (nodeA, nodeB)
		else:
			line = "%s -- %s" % (nodeA, nodeB)
		args_line = args
		if args_line and self.vertex_args:
			args_line += ", "
		if self.vertex_args:
			args_line += self.vertex_args
		if args_line:
			line += " [%s]" % args_line
		self._AddLine(line + ";")

	def AddComment(self, line):
		self._AddLine("// " + line)

	def AddCustomLine(self, line):
		self._AddLine(line)

# ###########################################

	def GraphAddArg(self, line):
		self._graph_args.append(line)

	def GraphEnter(self, graph_type):
		self._subgraph_depth = 0
		self._AddLine("%s {" % graph_type)
		for line in self._graph_args:
			self._AddLine(line)

	def GraphExit(self):
		while self._subgraph_depth > 0:
			self.SubgraphExit()
		self._AddLine("} // End of graph")

# ###########################################

	def SubgraphAddArg(self, line):
		self._subgraph_args.append(line)

	def SubgraphEnter(self, name):
		self._AddLine("subgraph %s {" % name)
		for line in self._subgraph_args:
			self._AddLine(line)
		if len(self.subgraph_colors):
			self._AddLine("color=%s" % self.subgraph_colors[self._subgraph_color_index])
			self._subgraph_color_index += 1
			if self._subgraph_color_index >= len(self.subgraph_colors):
				self._subgraph_color_index = 0
		self._subgraph_depth += 1

	def SubgraphExit(self):
		self._AddLine("}")
		self._subgraph_depth -= 1


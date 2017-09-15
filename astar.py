from queue import PriorityQueue
import math
import Node
from Node import State
from Node import Vehicle

class A_star_search:

	def __init__(self, start):
		self.start = start
		self.frontier = PriorityQueue() #Nodes
		self.open_nodes = []
		self.open_values = []
		self.closed = set()
		self.count = 0
		self.created = {} #(hashID, nodes) ##BRUKES IKKE

	def checkState(self, node):
		for i in range(0,len(self.open_nodes)):
			if self.open_nodes[i].getID() == node.getID():
				return True
		return False		
		

	def a_star_search(self):

		if self.start.check_Solution():
			return self.start, count	

		self.start.priority = 0 + self.start.heuristic()
		self.start.f_value = 0 + self.start.heuristic()
		self.frontier.put(self.start)
		self.open_nodes.append(self.start)
		self.created[self.start.getID()] = self.start

		while True:
			if self.frontier.empty():
				return False
			x = self.frontier.get()
			self.closed.add(x.getID())
			self.open_nodes.remove(x)
			#counting numbers of nodes considered
			self.count += 1
			if x.check_Solution():
				return x, count
			children = x.generateChildren()
			for c in children:
				print(self.count)
				print(c)
				#if c.getID() in self.created:
				#	c = self.created.get(c.getID())
				x.kids.append(c)
				if ((c.getID() not in self.closed) and (not self.checkState(c))):
					f = int(self.attach_and_eval(c,x))
					self.frontier.put(c)
					self.open_nodes.append(c)
				elif x.g_value + x.cost(c) < c.g_value:
					self.attach_and_eval(c,x)
					if c in self.open_nodes:
						sopen_nodes_temp = []
						for i in range(len(self.open_nodes)):
							open_nodes_temp.append(self.frontier.get())
						for i in range(len(open_nodes_temp)):
							open_nodes_temp[i].priority = open_nodes_temp[i].f_value
							self.frontier.put(open_nodes_temp[i])
					elif c in self.closed:
						self.propagate_path_improvements(c)

	def attach_and_eval(self, a,b):
		a.parent = b
		a.g_value = b.g_value + b.cost(a)
		a.f_value = a.g_value + a.heuristic()
		a.priority = int(a.f_value)
		return a.f_value

	def propagate_path_improvements(self, a):
		for c in a.kids:
			if a.g_value + a.cost(c) < c.g_value:
				c.parent = a
				c.g_value = a.g_value + a.cost(c)
				c.f_value = c.g_value + a.heuristic()

				propagate_path_improvements(c)

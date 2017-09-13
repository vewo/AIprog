from queue import PriorityQueue
import math
import Node
from Node import State
from Node import Vehicle

class A_star_search(object):



	def a_star_search(self, start):
		closed = []
		open_nodes = []
		frontier = PriorityQueue() #Nodes
		created = {} #(hashID, nodes)

		start.priority = 0 + start.heuristic()
		frontier.put(start) #g(S0)=0
		open_nodes.append(start)

		while True:
			if frontier.empty():
				return False
			x = frontier.get()
			closed.append(x)
			if x.check_Solution():
				return x
			children = x.generateChildren()
			for c in children:
				if c.getID() in created:
					c = created[created.get(c.getID())] #Probably not right
				else:
					created[c.getID()] = c
				x.kids.append(c)
				if not ((c in closed) or (c in open_nodes)):
					f = int(self.attach_and_eval(c,x))
					c.priority = int(f)
					frontier.put(c)
					open_nodes.append(c)
				if x.g_value + x.cost(x,c) < c.g_value():
					self.attach_and_eval(c,x)
					if c in open_nodes:
						open_nodes_temp = []
						for i in range(len(open_nodes)):
							open_nodes_temp.append(frontier.get())
						for i in range(len(open_nodes_temp)):
							open_nodes_temp[i].priority = open_nodes_temp[i].f_value
							frontier.put(open_nodes_temp[i])
					elif c in closed:
						self.propagate_path_improvements(c)

	def attach_and_eval(self, a,b):
		a.parent = b
		a.g_value = b.g_value + b.cost(a,b)
		a.f_value = a.g_value + a.heuristic()
		return a.f_value

	def propagate_path_improvements(self, a):
		for c in a.kids:
			if a.g_value + cost(a,c) < c.g_value:
				c.parent = a
				c.g_value = a.g_value + cost(a,c)
				c.f_value = c.g_value + a.heuristic()
				propagate_path_improvements(c)

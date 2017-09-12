from queue import PriorityQueue
import math
import Node
import State
import Vehicle

class A_star_search(object): 

	def a_star_search(graph, start):
		closed = []
		open_nodes = []
		frontier = PriorityQueue() #Nodes
		created = {} #(hashID, nodes)

		frontier.put(((0+start.heuristic(start, goal)), start)) #g(S0)=0
		open_nodes.append(start)

		while True: 
			if frontier.empty():
				return False
			x = frontier.get()[1]
			closed.add(x)
			if x.check_Solution():
				return x
			children = x.generateChildren()
			for c in children:
				if created.hasKey(c.getID()):
					c = created[created.get(c.getID())] #Probably not right
				else: 
					created.add(c.getID(), c)
				x.kids.add(c)
				if not ((c in closed) or (c in open_nodes)):
					f = attach_and_eval(c,x)
					frontier.put((f, c))
					open_nodes.append(c)
				elif x.g_value + x.cost(x,c) < c.g_value():
					attach_and_eval(c,x)
					if c in open_nodes:
						open_nodes_temp = []
						for i in range(len(open_nodes)):
							open_nodes_temp.append(frontier.get()[1])
						for i in range(len(open_nodes_temp)):
							frontier.put((open_nodes_temp[i].f_value, open_nodes_temp[i]))
					elif c in closed:
						propagate_path_improvements(c)

	def attach_and_eval(self, a,b):
		a.parent = b
		a.g_value = b.g_value + b.cost(a,b)
		a.f_value = a.g_value + a.heuristic(b)
		return a.f_value

	def propagate_path_improvements(self, a):
		for c in a.kids:
			if a.g_value + cost(a,c) < c.g_value:
				c.parent = a
				c.g_value = a.g_value + cost(a,c)
				c.f_value = c.g_value + a.heuristic(a)
				propagate_path_improvements(c)












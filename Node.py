
class Node(object):

	g_value = 0
	h_value = 0
	f_value = g_value + h_value
	parent = None
	kids = []
	priority = 0

	def __init__(self, state, parent):
		self.state = state
		self.parent = parent
		self.walls = [(4,3),(4,4)]

	def __lt__(self, other):
		return ((self.priority) < (other.priority))

	def __repr__(self):
		s = ""
		for v in self.state.vehicles:
			s+= "(" + str(v.no) + "," + str(v.orientation) + "," + str(v.x) + "," + str(v.y) + "," +  str(v.size) + "), "
		return s


	def heuristic(self):
		blocking = 0
		v0 = None
		for v in self.state.vehicles:
			if v.no == 0:
				v0 = v
			if v.orientation == 1:
				if (2 in range(v.y, v.y+v.size)):
					blocking += 1
		goalDistance = 4-v0.x
		return 0.5*goalDistance+0.5*blocking

	def getID(self):
		return self.state.getID()

	def generateChildren(self):
		children = []
		i = 0
		for v in self.state.vehicles:
			i+=1
			if v.orientation == 0:
				if (self.state.isAvailable(v.x-1,v.y)):
					kidState = list(self.state.vehicles)
					kidState.remove(v)
					newCarPosition = Vehicle(v.no, v.orientation, v.x-1, v.y, v.size)
					kidState.insert(v.no, newCarPosition)
					kid = Node(State(kidState), self)
					children.append(kid)
				if (self.state.isAvailable(v.x+v.size, v.y)):
					kidState = list(self.state.vehicles)
					del kidState[self.state.vehicles.index(v)]
					newCarPosition = Vehicle(v.no, v.orientation, v.x+1, v.y, v.size)
					kidState.insert(v.no, newCarPosition)
					kid = Node(State(kidState), self)
					children.append(kid)
			elif v.orientation == 1:
				if (self.state.isAvailable(v.x, v.y+1)):
					kidState = list(self.state.vehicles)
					kidState.remove(v)
					newCarPosition = Vehicle(v.no, v.orientation, v.x, v.y-1, v.size)
					kidState.insert(v.no, newCarPosition)
					kid = Node(State(kidState), self)
					children.append(kid)
				if (self.state.isAvailable(v.x, v.y+v.size)):
					kidState = list(self.state.vehicles)
					kidState.remove(v)
					newCarPosition = Vehicle(v.no, v.orientation, v.x, v.y+1, v.size)
					kidState.insert(v.no, newCarPosition)
					kid = Node(State(kidState), self)
					children.append(kid)
		return children


	def check_Solution(self):
		return (((self.state.vehicles[0].x + self.state.vehicles[0].size - 1) == 5) and (self.state.vehicles[0].y == 2))

	def cost(self, b):
		return 1



class State(object):

	vehicles = []
	s = ""


	def __init__(self, vehicles):
	    self.vehicles = vehicles
	    for v in vehicles:
	    	self.s += str(v.no) + str(v.orientation) + str(v.x) + str(v.y) + str(v.size)

	def getID(self):
		return hash(self.s)

	def isAvailable(self, x, y):
		if x < 0 or x > 5:
			return False
		if y < 0 or y > 5:
			return False
		for v in self.vehicles:
			if v.orientation == 0:
				if (v.y == y) and (x in range(v.x, v.x+v.size)):
					return False
			elif v.orientation == 1:
				if (v.x == x) and (y in range(v.y, v.y+v.size)):
					return False
		return True




class Vehicle(object):

	def __init__(self, no, orientation, x,y,size):
	    self.no = no
	    self.orientation = orientation
	    self.x = x
	    self.y = y
	    self.size = size

	def __repr__(self):
		s = ""
		s+= "(" + str(self.no) + "," + str(self.orientation) + "," + str(self.x) + "," + str(self.y) + "," +  str(self.size) + "), "
		return s

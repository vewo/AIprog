
class Node(object):

	g_value = 0
	h_value = 0
	f_value = g_value + h_value
	status = Open
	parent = None
	kids = []

	def __init__(self, state, parent):
	    self.state = state
	    self.parent = parent
	    self.walls = [(4,3),(4,4)]


	def heuristic(self, b):
	    goalDistance = 4-self.state.vehicles[0].x
	    return math.sqrt((x1 - x2)**2) + math.sqrt((y1 - y2)**2) #Manhattan distance

	def getID(self):
		return self.state.hashID()

	def generateChildren(self): 
		children = []
		for v in self.state.vechicles:
			if v.orientation = 0:
				if (self.state.isAvailable(v.x-1, v.y)):
					kidState = self.state.vehicles
					kidState.remove(v)
					newCarPosition = Vehicle(v.no, v.orientation, v.x-1, v.y, v.size)
					kidState.insert(v.no, newCarPosition)
					kid = Node(kidState, self)
					children.append(kid)
				if (self.state.isAvailable(v.x+v.size, v.y)):
					kidState = self.state.vehicles
					kidState.remove(v)
					newCarPosition = Vehicle(v.no, v.orientation, v.x+1, v.y, v.size)
					kidState.insert(v.no, newCarPosition)
					kid = Node(kidState, self)
					children.append(kid)
			elif v.orientation = 1:
				if (self.state.isAvailable(v.x, v.y+1)):
					kidState = self.state.vehicles
					kidState.remove(v)
					newCarPosition = Vehicle(v.no, v.orientation, v.x, v.y-1, v.size)
					kidState.insert(v.no, newCarPosition)
					kid = Node(kidState, self)
					children.append(kid)
				if (self.state.isAvailable(v.x, v.y+size)):
					kidState = self.state.vehicles
					kidState.remove(v)
					newCarPosition = Vehicle(v.no, v.orientation, v.x, v.y+1, v.size)
					kidState.insert(v.no, newCarPosition)
					kid = Node(kidState, self)
					children.append(kid)
		return children


	def check_Solution(self):
		return (((self.state.vechicles[0].x + self.state.vechicles[0].size - 1) == 5) and (self.state.vechicles[0].y == 2))

	def cost(a,b):
		return 1



class State(object):

	vehicles = []

	def __init__(self, vehicles):
	    self.vehicles = vehicles

	def hashID(self):
		hashID = 0
		for v in vehicles:
			hashID += (3*v.no + 13*v.x + 17*v.y + 107*size) #Is this really a good hash??

	def isAvailable(x,y):
		for v in self.vehicles:
			if v.orientation = 0:
				if (v.y = y) and (x in range(v.x, v.x+size)):
					return False
			elif v.orientation = 1:
				if (v.x = x) and (y in range(v.y, v.y+size)):
					return False
			return True




class Vehicle(object):

	def __init__(self, no, orientation, x,y,size):
	    self.no = no
	    self.orientation = orientation
	    self.x = x
	    self.y = y
	    self.size = size

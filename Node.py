
class Node(object):

	g_value = 0
	h_value = 0
	f_value = g_value + h_value
	#status = Open
	parent = None
	kids = []

	def __init__(self, state, parent):
	    self.state = state
	    self.parent = parent
	    self.walls = [(4,3),(4,4)]


	def heuristic(self, b):
	    (x1, y1) = a
	    (x2, y2) = b
	    #return abs(x1 - x2) + abs(y1 - y2)
	    return math.sqrt((x1 - x2)**2) + math.sqrt((y1 - y2)**2) #Manhattan distance

	def getID(self):
		return self.state.hashID()

	def generateChildren(self):
		children = []
		for v in self.state.vechicles:
			break

	def check_Solution(self):
		return (((self.state.vechicles[0].x + self.state.vechicles[0].size - 1) == 5) and (self.state.vechicles[0].y == 2))

	def cost(a,b):
		return 1



class State(object):

	vehicles = []

	def __init__(self):
	    self.no = no
	    self.orientation = orientation
	    self.x = x
	    self.y = y

	def hashID(self):
		hashID = 0
		for v in vehicles:
			hashID += (3*v.no + 13*v.x + 17*v.y + 107*size) #Is this really a good hash??



class Vehicle(object):

	def __init__(self, orientation, x,y,size, no):
		self.orientation = orientation
		self.x = x
		self.y = y
		self.size = size
		self.no = no

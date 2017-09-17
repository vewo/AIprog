from General import Node, State
import copy


class NGNode(Node):
	def __init__(self, state, parente):
		super(NGNode, self).__init__(state, parent)


class NGState(State):
	def __init__(self, state):
		super(NGState, self).__init__(state)


	def initialize(self, state):
		rows = []
		columns = []
		for i in range(len(state[0])):
			rows.append(Variable(0, state[0][i], len(state[0])))
		for i in range(len(state[1])):
			columns.append(Variable(1, state[1][i], len(state[1])))
		return [rows, columns]

	def getID(self):
		pass



class Variable():
	def __init__(self, type, segmentSizes, varLength):
		self.type = type
		self.segmentSizes = segmentSizes
		self.domain = self.get_permutations(segmentSizes, varLength)


	def get_permutations(self, segmentSizes, varLength):
	#no segments
		if len(segmentSizes) == 0:
			row = []
			for x in range(varLength):
				row.append(False)
			return [row]

		permutations = []
	    
		for start in range(varLength - segmentSizes[0] + 1):
		    permutation = []
		    for x in range(start):
		        permutation.append(False)
		    for x in range(start, start + segmentSizes[0]):
		        permutation.append(True)
		    x = start + segmentSizes[0]
		    if x < varLength:
		        permutation.append(False)
		        x += 1
		    if x == varLength and len(segmentSizes) == 0:
		        permutations.append(permutation)
		        break
		    sub_start = x
		    sub_rows = self.get_permutations(segmentSizes[1:len(segmentSizes)], varLength - sub_start)
		    for sub_row in sub_rows:
		        sub_permutation = copy.deepcopy(permutation)
		        for x in range(sub_start, varLength):
		            sub_permutation.append(sub_row[x-sub_start])
		        permutations.append(sub_permutation)
		return permutations


class Solver():
	def __init__(self, board):
		if board.split('.')[1] == "txt":
			brd = self.makeNewBoard(board)
			self.first_node = NGState(brd) #Setting state
		else:
			print("unsupported input, give either a predefined level or a textfile as an argument")

	def makeNewBoard(self, board):
	    rows = []
	    columns = []
	    with open(board) as infile:
	    	firstLine = infile.readline().split(' ')
	    	noCols = int(firstLine[0])
	    	noRows = int(firstLine[1])
	    	for i in range(noRows):
	    		rowLine = infile.readline().strip("\n").split(" ")
	    		row = []
	    		for ss in rowLine: 
	    			row.append(int(ss))
	    		rows.append(row)
	    	for i in range(noCols):
	    		colLine = infile.readline().strip("\n").split(" ")
	    		col = []
	    		for ss in colLine: 
	    			col.append(int(ss))
	    		columns.append(col)
	    return [rows, columns]



	def solve(self):
		pass


s = Solver("cat.txt")
print(s)



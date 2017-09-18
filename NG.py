from General import Node, State
import copy


class NGNode(Node):
	def __init__(self, state, parent):
		super(NGNode, self).__init__(state, parent)


class NGState(State):
	def __init__(self, state):
		super(NGState, self).__init__(state)


	def initialize(self, state):
		rows = []
		columns = []
		for i in range(len(state[0])):
			rows.append(Variable(0, state[0][i], len(state[1])))
		for i in range(len(state[1])):
			columns.append(Variable(1, state[1][i], len(state[0])))
		return [rows, columns]

	def getID(self):
		pass



class Variable():
	def __init__(self, type, segmentSizes, varLength):
		self.type = type
		self.segmentSizes = segmentSizes
		self.domain = self.get_permutations(segmentSizes, varLength)
		self.varLength = varLength


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
		self.brd = self.makeNewBoard(board)
		self.first_node = NGState(self.brd)
		#if board.split('.')[1] == "txt":
		#	self.brd = self.makeNewBoard(board)
		#	self.first_node = NGState(brd) #Setting state
		#else:
		#	print("unsupported input, give either a predefined level or a textfile as an argument")

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
f = s.first_node

rowDomain = []
for i in range(len(f.state[0])):
	rowDomain += (f.state[0][i].domain)
columnDomain = []
for i in range(len(f.state[1])):

	columnDomain += (f.state[1][i].domain)


#ROWS
fixedPointsRow = []
for rowNo in range(len(f.state[0])):
	domain = f.state[0][rowNo].domain #Get domain for variable
	fillRate = []
	fillRate = [0]*(f.state[0][rowNo].varLength)
	#number of true in each index
	for permutation in domain:
		for index in range(len(permutation)):
			if permutation[index] == True:
				fillRate[index] += 1
	for index in range(len(fillRate)):
		if fillRate[index] == len(domain):
			fixedPointsRow.append((rowNo, index, 1))
		if fillRate[index] == len(domain):
			fixedPointsRow.append((rowNo, index, 1))
print(fixedPointsRow)
#COLUMNS
fixedPointsColumn = []
for columnNo in range(len(f.state[1])):
	domain = f.state[1][columnNo].domain #Get domain for variable
	fillRate = []
	fillRate = [0]*(f.state[1][columnNo].varLength)
	#number of true in each index
	for permutation in domain:
		for index in range(len(permutation)):
			if permutation[index] == True:
				fillRate[index] += 1
	for index in range(len(fillRate)):
		if fillRate[index] == len(domain):
			fixedPointsColumn.append((index, columnNo, 1))
print(fixedPointsColumn)


#print(columnDomain)

var = f.state[0][0].domain # [kolonne/rad] [index]

indexList = []
indexList = [0]*len(rowDomain[0])
#number of true in each index
for i in var:
	for j in range(len(i)):
		if i[j] == True:
			indexList[j] += 1





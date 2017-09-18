from General import Node, State
import copy


class NGNode(Node):
	def __init__(self, state, parent):
		super(NGNode, self).__init__(state, parent)


class NGState(State):
	def __init__(self, board):
		super(NGState, self).__init__(board)


	def initialize(self, state):
		rows = []
		columns = []
		for i in range(len(state[0])):
			rows.append(Variable(0, state[0][i], len(state[1])))
		for i in range(len(state[1])):
			segmentSizes = copy.deepcopy(state[1][i])
			segmentSizes.reverse()
			columns.append(Variable(1, segmentSizes, len(state[0])))
		return [rows, columns]

	def getState(self):
		domainSize = 0
		for row in self.state[0]:
			domainSize += len(row.domain)
		for col in self.state[1]:
			domainSize += len(col.domain)
		return(domainSize)


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


def getRowDomain(state):
	rowDomain = []
	for i in range(len(state[0])):
		rowDomain.append((state[0][i].domain))
		#rowDomain += (state[0][i].domain)
	return rowDomain
	

def getColDomain(state):
	columnDomain = []
	for i in range(len(state[1])):
		columnDomain.append(state[1][i].domain)
		#columnDomain += (state[1][i].domain)
	return columnDomain





def getFixedRows(state):
#ROWS
	fixedPointsRow = []
	for rowNo in range(len(state[0])):
		domain = state[0][rowNo].domain #Get domain for row
		fillRate = [0]*(state[0][rowNo].varLength)
		#number of true in each index
		for permutation in domain:
			for index in range(len(permutation)):
				if permutation[index] == True:
					fillRate[index] += 1
		for index in range(len(fillRate)):
			if fillRate[index] == len(domain):
				fixedPointsRow.append((rowNo, index, 1))
			if fillRate[index] == 0:
				fixedPointsRow.append((rowNo, index, 0))
	return fixedPointsRow
	

def getFixedColumns(state):
	fixedPointsColumn = []
	for columnNo in range(len(state[1])):
		domain = state[1][columnNo].domain #Get domain for column
		fillRate = [0]*(state[1][columnNo].varLength)
		#number of true in each index
		for permutation in domain:
			for index in range(len(permutation)):
				if permutation[index] == True:
					fillRate[index] += 1
		for index in range(len(fillRate)):
			if fillRate[index] == len(domain):
				fixedPointsColumn.append((index, columnNo, 1))
			if fillRate[index] == 0:
				fixedPointsColumn.append((index, columnNo, 0))
	return fixedPointsColumn
	

def domainFiltering(fixedPoints, domain, mode):
	
	changed = False

	if mode == "rowCheck":
		for fixedPoint in fixedPoints:
			toBeDeleted = []
			yOfFixedPoint = fixedPoint[0] #Row number of fixed point
			xOfFixedPoint = fixedPoint[1] #Index of fixed point
			permutations = domain[yOfFixedPoint] #Permutations of the row of interest
			for permutation in permutations:
				if permutation[xOfFixedPoint] != fixedPoint[2]:
					toBeDeleted.append(permutation)
					changed = True
			for delete in toBeDeleted:
				domain[yOfFixedPoint].remove(delete)
	elif mode == "colCheck":
		for fixedPoint in fixedPoints:
			toBeDeleted = []
			yOfFixedPoint = fixedPoint[0] #Column number of fixed point
			xOfFixedPoint = fixedPoint[1] #Index of fixed point
			permutations = domain[xOfFixedPoint] #Permutations on index from fixedpoint
			for permutation in permutations:
				if permutation[yOfFixedPoint] != fixedPoint[2]:
					toBeDeleted.append(permutation)
					changed = True
			for delete in toBeDeleted:
				domain[xOfFixedPoint].remove(delete)
	return changed

def revise(NGstate):
	domainFiltering(getFixedColumns(NGstate.state), getRowDomain(NGstate.state), "rowCheck")
	domainFiltering(getFixedRows(NGstate.state), getColDomain(NGstate.state), "colCheck")
	changed = True
	while True: 
		changed = domainFiltering(getFixedColumns(NGstate.state), getRowDomain(NGstate.state), "rowCheck")
		if changed == False: 
			break
		changed = domainFiltering(getFixedRows(NGstate.state), getColDomain(NGstate.state), "colCheck")
		if changed == False: 
			break
	print("solution", NGstate.getState())
	return NGstate.getState()

s = Solver("chick.txt")
NGState = s.first_node
revise(NGState)

#var = Variable(0, [1], 10)
#print(len(var.get_permutations([50],50)))


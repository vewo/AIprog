from General import Node, State
import copy


class NGNode(Node):
	def __init__(self, state, parent):
		super(NGNode, self).__init__(state, parent)

	def isSolution(self):
		return (self.state.getTotalNoOfPermutations() == (len(self.state.state[0]) + len(self.state.state[1])))

	def heuristic(self):
		return (self.state.getTotalNoOfPermutations()-(len(self.state.state[0]) + len(self.state.state[1])))

	def cost(self, parent):
		return 0

	def createChildren(self):
		assumptionVar = self.state.getSmallestTooLargeDomain()
		children = []
		for i in range(assumptionVar[2]):
			child = NGNode(copy.deepcopy(self.state), self)
			child.state.state[assumptionVar[0]][assumptionVar[1]].domain = [child.state.state[assumptionVar[0]][assumptionVar[1]].domain[i]]
			#print(child.state.state)
			child.state.GAC()
			self.f_value = self.heuristic()
			children.append(child)
		return children


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

	def getID(self): #unique identifier for the state
		t = tuple()
		for row in self.getRowDomain():
			for permutation in row:
				t += tuple(permutation)
		for col in self.getColDomain():
			for permutation in col:
				t += tuple(permutation)
		return hash(t)


	def getTotalNoOfPermutations(self): #return the total number of values the variables can take
		domainSize = 0
		for row in self.state[0]:
			domainSize += len(row.domain)
		for col in self.state[1]:
			domainSize += len(col.domain)
		return domainSize

	def getRowDomain(self):
		rowDomain = []
		for i in range(len(self.state[0])):
			rowDomain.append((self.state[0][i].domain))
		return rowDomain


	def getColDomain(self):
		columnDomain = []
		for i in range(len(self.state[1])):
			columnDomain.append(self.state[1][i].domain)
		return columnDomain


	def getFixedRows(self):
	#ROWS
		fixedPointsRow = []
		for rowNo in range(len(self.state[0])):
			domain = self.state[0][rowNo].domain #Get domain for row
			fillRate = [0]*(self.state[0][rowNo].varLength)
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
	

	def getFixedColumns(self):
		fixedPointsColumn = []
		for columnNo in range(len(self.state[1])):
			domain = self.state[1][columnNo].domain #Get domain for column
			fillRate = [0]*(self.state[1][columnNo].varLength)
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
	

	def revise(self, mode):
		
		changed = False

		if mode == "rowCheck":
			domain = self.getRowDomain()
			for fixedPoint in self.getFixedColumns():
				toBeDeleted = []
				yOfFixedPoint = fixedPoint[0] #Row number ofs fixed point
				xOfFixedPoint = fixedPoint[1] #Index of fixed point
				permutations = domain[yOfFixedPoint] #Permutations of the row of interest
				for permutation in permutations:
					if permutation[xOfFixedPoint] != fixedPoint[2]:
						toBeDeleted.append(permutation)
						changed = True
				for delete in toBeDeleted:
					domain[yOfFixedPoint].remove(delete)
		elif mode == "colCheck":
			domain = self.getColDomain()
			for fixedPoint in self.getFixedRows():
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

	def GAC(self):
		self.revise("rowCheck")
		self.revise("colCheck")
		changed = True
		while True: 
			changed = self.revise("rowCheck")
			if changed == False: 
				break
			changed = self.revise("colCheck")
			if changed == False: 
				break

	def getSmallestTooLargeDomain(self):
		rowDomain = self.getRowDomain()
		colDomain = self.getColDomain()
		smallest = (0,0,1000)
		for row in sorted(rowDomain, key = len):
			if ((len(row) >1) and (len(row) < smallest[2])):
				smallest = (0, rowDomain.index(row), len(row))
		for col in sorted(colDomain, key = len):
			if ((len(col) >1) and (len(col) < smallest[2])):
				smallest = (1, colDomain.index(col), len(col))
		if(smallest[2]) == 1000:
			smallest = (0,0,0)
		return smallest





class Variable():
	def __init__(self, type, segmentSizes, varLength):
		self.type = type
		self.segmentSizes = segmentSizes
		self.domain = self.get_permutations(segmentSizes, varLength)
		self.varLength = varLength

	def __repr__(self):
		s = ""
		for i in self.domain:
			s += str(i)
		return(s)


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
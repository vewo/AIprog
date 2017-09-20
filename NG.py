from General import Node, State
import copy

class NGNode(Node):
	#Initializes node from superclass
	def __init__(self, state, parent):
		super(NGNode, self).__init__(state, parent)

	#Nonogram specific check for solution
	def isSolution(self):
		return (self.state.getTotalNoOfPermutations() == (len(self.state.state[0]) + len(self.state.state[1])))

	##Nonogram specific heuristic
	def heuristic(self):
		return (self.state.getTotalNoOfPermutations()-(len(self.state.state[0]) + len(self.state.state[1])))

	#Nonogram specific cost
	def cost(self, parent):
		return ((len(self.state.state[0]) + len(self.state.state[1])))

	#Nonogram specific method for creating children
	def createChildren(self):
		assumptionVar = self.state.getSmallestTooLargeDomain()
		children = []
		for i in range(assumptionVar[2]):
			child = NGNode(copy.deepcopy(self.state), self)
			child.state.state[assumptionVar[0]][assumptionVar[1]].domain = [child.state.state[assumptionVar[0]][assumptionVar[1]].domain[i]]
			child.state.GAC()
			self.f_value = self.heuristic()
			children.append(child)
		return children


class NGState(State):
	#Initializes from superclass
	def __init__(self, board):
		super(NGState, self).__init__(board)


	#Nonogram specific initialization method
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

	#Returns a unique identifier for the state
	def getID(self): 
		s = ""
		for row in self.getRowDomain():
			for permutation in row:
				t = ''.join(str(samma) for samma in permutation)
				s+= t
		for col in self.getColDomain():
			for permutation in col:
				t = ''.join(str(samma) for samma in permutation)
				s+= t
		return hash(s)


	#Returns the total number of values the variables can take
	def getTotalNoOfPermutations(self): 
		domainSize = 0
		for row in self.state[0]:
			domainSize += len(row.domain)
		for col in self.state[1]:
			domainSize += len(col.domain)
		return domainSize

	#Returns the domain of a given row
	def getRowDomain(self):
		rowDomain = []
		for i in range(len(self.state[0])):
			rowDomain.append((self.state[0][i].domain))
		return rowDomain

	#Returns the domain of a given column
	def getColDomain(self):
		columnDomain = []
		for i in range(len(self.state[1])):
			columnDomain.append(self.state[1][i].domain)
		return columnDomain


	#Returns a list of tuples with row number, index and value of a cell that
	#given the domain, only can have one value.
	def getFixedRows(self):
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
	
	#Returns a list of tuples with column number, index and value of a cell that
	#given the domain, only can have one value.
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
	
	#Using the constraints, eliminates variables from the domain that don't
	#satisfy the constraints
	def revise(self, mode):		
		changed = False
		#Prunes the row domain
		if mode == "rowCheck":
			domain = self.getRowDomain()
			for fixedPoint in self.getFixedColumns():
				toBeDeleted = []
				yOfFixedPoint = fixedPoint[0] #Row number of fixed point
				xOfFixedPoint = fixedPoint[1] #Index of fixed point
				permutations = domain[yOfFixedPoint] #Permutations of the row of interest
				for permutation in permutations:
					if permutation[xOfFixedPoint] != fixedPoint[2]:
						toBeDeleted.append(permutation)
				for delete in toBeDeleted:
					domain[yOfFixedPoint].remove(delete)
					changed = True
		#Prunes the column domain
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
				for delete in toBeDeleted:
					domain[xOfFixedPoint].remove(delete)
					changed = True
		return changed

	#Runs Revise until no furthing pruning of th domain is possible
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

	#Returns the domain that is the best candidate for making an assumption
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
	#Initialization
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

	#Returns the allowed permutations for a variable given its segments, and dimension
	def get_permutations(self, segmentSizes, varLength): #segmentSizes = list of the size of the segments to be placed, varLength = length of row/column to place segments in
		#True means the cell chould be filled, False means unfilled
		if len(segmentSizes) == 0:  #if there are no segments to be placed
			fillingList = []
			for i in range(varLength): #the length of the row/column to be filled 
				fillingList.append(False) #all cells are empty
			return [fillingList]

		allPerm = [] #the final set of possible fillings of the row/column

		for possibleStartIndex in range(varLength - segmentSizes[0]+1): #Yields all possible start indices for the first segment in the segmentSizes input variable
			perm = []
			for unfilled in range(possibleStartIndex): #Fill with False until the segment start
				perm.append(False)
			for filled in range(possibleStartIndex, possibleStartIndex+segmentSizes[0]): #Fill inn the cells of the segment with True
				perm.append(True)
			nextIndex = possibleStartIndex + segmentSizes[0] #index of the cell adjacent to where the segment ends
			if nextIndex < varLength: #Still cells to be filled out, either with segments or with False (or combination)
				perm.append(False) #needs to be at least one space between two segments
				nextIndex += 1
			if nextIndex == varLength and len(segmentSizes) == 0: #the last segment is filled out, and we have filled the whole row/column
				allPerm.append(perm)
				break
			subStart = nextIndex
			subVariables = self.get_permutations(segmentSizes[1:len(segmentSizes)], varLength-subStart) #returns all possible ways to fill out the remaining segments (if any) in the reminder of the row/column
			for subVariable in subVariables:
				subPerm = copy.deepcopy(perm)
				for i in range(subStart, varLength):
					subPerm.append(subVariable[i-subStart])
				allPerm.append(subPerm)
		return allPerm


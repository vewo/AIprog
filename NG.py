from General import Node, State
import copy


class NGNode(Node):
	def __init__(self, state, parente):
		super(NGNode, self).__init__(state, parent)


class NGState(State):
	def __init__(self, state):
		super(NGState, self).__init__(state)

	def initialize(self, state):
		pass

	def getID(self):
		pass



class Variable():
	def __init(self, type, segmentSizes, domain, varLength):
		self.type = type
		self.segmentSizes = segmentSizes
		self.domain = get_permutations(self, segmentSizes, varLength)


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
	    sub_rows = get_permutations(segmentSizes[1:len(segmentSizes)], varLength - sub_start)
	    for sub_row in sub_rows:
	        sub_permutation = copy.deepcopy(permutation)
	        for x in range(sub_start, varLength):
	            sub_permutation.append(sub_row[x-sub_start])
	        permutations.append(sub_permutation)
	return permutations


class Solver():


	cat = 
			[[8, 9],
			[5],
			[3, 1],
			[2, 2],
			[1, 1],
			[1, 1],
			[5],
			[5],
			[3],
			[1, 1],
			[2],
			[4],
			[8],
			[4, 3],
			[2, 2],
			[1],
			[3],
			[3]]






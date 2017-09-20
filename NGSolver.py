import copy
from NG import NGNode, NGState, Variable
from astar import A_star
from NGGUI import NGApp


class NGSolver():
	#Initialize
	def __init__(self, board):
		self.brd = self.makeNewBoard(board)
		self.start_state = NGState(self.brd)
		if board.split('.')[1] == "txt":
			print("initiated succesfully")
		else:
			print("unsupported input, give either a predefined level or a textfile as an argument")

	#Reads from file and returns the a list with rows and columns
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

	#Runs revise on start node, checks if it has found the solution, if not, runs A* search on the node.
	def A_Star_GAC(self, NGstate):
		NGState.GAC()
		start_node = NGNode(NGstate, None)
		#Checking if the domain is reduced enough to have unique solution
		if not (start_node.isSolution()): 
			solution = A_star(start_node.state, NGNode)
			solutionNode, noGenerated, noExplored, explored_nodes = solution.a_star_search()
			app = NGApp(explored_nodes, solutionNode.path(), True)
			app.mainloop()
		else: 
			app = NGApp([], start_node.path(), False)
			app.mainloop()


s = NGSolver("nonoboards/heart.txt")
NGState = s.start_state
s.A_Star_GAC(NGState)


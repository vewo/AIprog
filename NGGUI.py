import tkinter as tk

class NGApp(tk.Tk):

	#Initialize
	def __init__(self, explored, solution_path, astar):
		tk.Tk.__init__(self)
		self.explored = explored
		self.solution_path = solution_path
		self.solution_counter = 0
		self.counter = 0
		self.astar = astar

		self.rows = len(solution_path[0].state.state[0])
		self.columns = len(solution_path[0].state.state[1])
		self.ratio = self.columns/self.rows
		self.width = int(600*self.ratio)
		self.height = 600
		self.canvas = tk.Canvas(self, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
		self.canvas.pack(side="top", fill="both", expand="true")
		self.cellwidth = self.width/self.columns
		self.cellheight = self.height/self.rows
		self.delay = int(10000/len(self.explored))

		self.rect = {}
		for column in range(self.columns):
			for row in range(self.rows):
				x1 = column*self.cellwidth
				y1 = row * self.cellheight
				x2 = x1 + self.cellwidth
				y2 = y1 + self.cellheight
				self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
		

		self.var = tk.StringVar()
		label = tk.Label(self, textvariable=self.var)

		self.var.set("Are you ready")
		label.pack()

		self.redraw(self.delay)


	
	def redraw(self, delay, display_solution = False):
		tempBoard = list()
		if self.astar:
			if display_solution:
				fixedPoints = self.solution_path[self.solution_counter].state.getFixedRows()
				tempBoard = [["x" for _ in range(self.columns)] for _ in range(self.rows)]
				for fixedPoint in fixedPoints:
					tempBoard[fixedPoint[0]][fixedPoint[1]] = fixedPoint[2]
				tempBoard.reverse()
				self.solution_counter += 1
			else:
				fixedPoints = self.explored[self.counter].state.getFixedRows()
				tempBoard = [["x" for _ in range(self.columns)] for _ in range(self.rows)]
				for fixedPoint in fixedPoints:
					tempBoard[fixedPoint[0]][fixedPoint[1]] = fixedPoint[2]
				tempBoard.reverse()
		else:
			print(self.solution_path)
			fixedPoints = self.solution_path[0].state.getFixedRows()
			tempBoard = [["x" for _ in range(self.columns)] for _ in range(self.rows)]
			for fixedPoint in fixedPoints:
				tempBoard[fixedPoint[0]][fixedPoint[1]] = fixedPoint[2]
			tempBoard.reverse()
		self.canvas.itemconfig("rect", fill="white")
		for i, row in enumerate(tempBoard): #  hack, index
			for j, column in enumerate(row): # hack, index
				item_id = self.rect[i, j]
				if tempBoard[i][j] == 1:
					self.canvas.itemconfig(item_id, fill="#000000")
				elif tempBoard[i][j] == 0:
					self.canvas.itemconfig(item_id, fill="#FFFFFF")
				else:
					self.canvas.itemconfig(item_id, fill="#A9A9A4")
		self.counter += 1
		if(self.astar and self.counter < len(self.explored)):
			self.var.set("State number" + str((self.counter)) + "/" + str(len(self.explored)-1))
			self.after(delay, lambda: self.redraw(delay))
		elif(self.counter == len(self.explored)):
			input()
			self.counter += 1
			self.after(delay, lambda: self.redraw(delay, display_solution=True))
		elif(self.astar and self.solution_counter < len(self.solution_path)):
			input()
			self.delay = int(10000/len(self.solution_path))
			self.var.set("State number" + str((self.solution_counter)) + "/" + str(len(self.solution_path)-1))
			self.after(delay, lambda: self.redraw(delay, display_solution=True))



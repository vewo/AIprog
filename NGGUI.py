import tkinter as tk

class NGApp(tk.Tk):

	def __init__(self, nodes, solution):
		tk.Tk.__init__(self)
		self.nodes = nodes
		self.solution = solution
		self.solution_counter = 0
		self.counter = 0

		self.colors = ["#000000", "#A9A9A4", "#FFFFFF"]

		self.rows = len(solution.state.state[0])
		self.columns = len(solution.state.state[1])
		self.ratio = self.columns/self.rows
		self.width = 600*self.ratio
		self.height = 600
		self.canvas = tk.Canvas(self, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
		self.canvas.pack(side="top", fill="both", expand="true")
		self.cellwidth = self.width/self.columns
		self.cellheight = self.height/self.rows

		self.rect = {}
		for column in range(self.columns):
		    for row in range(self.rows):
		        x1 = column*self.cellwidth
		        y1 = row * self.cellheight
		        x2 = x1 + self.cellwidth
		        y2 = y1 + self.cellheight
		        self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")

		self.redraw(100)

	'''
	def drawWhite(self, delay):
		tempBoard = [["x"]*6]*6
	    self.canvas.itemconfig("rect", fill="white")
	    for i, row in enumerate(tempBoard): #  hack, index
	        for j, column in enumerate(row): # hack, index
	            item_id = self.rect[i,j]
	            if tempBoard[j][i] == "x":
	                self.canvas.itemconfig(item_id, fill="white")
	'''



	def redraw(self, delay, display_solution = True):
	    tempBoard = list()
	    if display_solution:
	        for row in self.solution.state.state[0]:
	        	tempBoard.append(row.domain[0])
	        tempBoard.reverse()
	        self.solution_counter +=1
	    else:
	        tempBoard = self.nodes[self.counter].state.getGrid()
	    self.canvas.itemconfig("rect", fill="white")
	    for i, row in enumerate(tempBoard): #  hack, index
	        for j, column in enumerate(row): # hack, index
	            item_id = self.rect[i, j]

	            if tempBoard[i][j]:
	                self.canvas.itemconfig(item_id, fill="black")
	            else:
	                self.canvas.itemconfig(item_id, fill="white")
	    self.counter += 1
	    #if(self.counter < len(self.nodes)):
	    #    self.after(delay, lambda: self.redraw(delay))
	    #elif(self.counter == len(self.nodes) and (self.solution_counter == 0)):
	    #	print("Kommer hit")
	    #	self.after(1000, lambda: self.drawWhite(1000))
	    self.after(delay, lambda: self.redraw(delay, display_solution=True))



import tkinter as tk

class RHApp(tk.Tk):

    def __init__(self, explored, solution_path, display):
        tk.Tk.__init__(self)
        self.explored = explored
        self.solution_path = solution_path
        self.solution_counter = 0
        self.counter = 0

        self.colors = ["#FF0000", "#000080", "#CD5C5C", "#FFA07A", "#008000", "#00FFFF", "#008080", "#0000FF","#00FF00", "#808000", "#808080", "#000000", "#800080", "#FFFF00", "#800000", "#33FF7A", "#BB33FF", "#FFAC33"]

        self.canvas = tk.Canvas(self, width=600, height=600, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 6
        self.columns = 6
        self.cellwidth = 100
        self.cellheight = 100
        self.delay = int(10000/len(self.explored))

        self.rect = {}
        for column in range(6):
            for row in range(6):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue", tags="rect")

        self.var = tk.StringVar()
        label = tk.Label(self, textvariable=self.var)

        self.var.set("Are you ready")
        label.pack()

        self.redraw(self.delay, display_solution=display)


    def redraw(self, delay, display_solution = False):
        tempBoard = list()
        if display_solution:
            tempBoard = self.solution_path[self.solution_counter].state.getGrid()
            self.solution_counter +=1
        else:
            tempBoard = self.explored[self.counter].state.getGrid()
        self.canvas.itemconfig("rect", fill="white")
        for i, row in enumerate(tempBoard): #  hack, index
            for j, column in enumerate(row): # hack, index
                item_id = self.rect[i,j]
                if tempBoard[j][i] == "x":
                    self.canvas.itemconfig(item_id, fill="white")
                else:
                    self.canvas.itemconfig(item_id, fill=self.colors[tempBoard[j][i]])
        self.counter += 1
        if(not display_solution and self.counter < len(self.explored)):
            self.var.set("State number" + str((self.counter)) + "/" + str(len(self.explored)-1))
            self.after(delay, lambda: self.redraw(delay))
        elif(self.counter == len(self.explored)):
            input()
            self.counter += 1
            self.after(delay, lambda: self.redraw(delay, display_solution=True))
        elif(self.solution_counter < len(self.solution_path)):
            delay = int(10000/len(self.solution_path))
            self.var.set("State number" + str((self.solution_counter)) + "/" + str(len(self.solution_path)-1))
            self.after(delay, lambda: self.redraw(delay, display_solution=True))



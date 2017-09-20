from RH import RHNode, RHState
from astar import A_star
from RHGUI import RHApp

class RHSolver():

    def __init__(self, level):
        if level == "easy":
            self.first_node = A_star(RHState(self.easy), RHNode)
        elif level == "medium":
            self.first_node = A_star(RHState(self.medium), RHNode)
        elif level == "hard":
            self.first_node = A_star(RHState(self.hard), RHNode)
        elif level == "expert":
            self.first_node = A_star(RHState(self.expert), RHNode)
        elif level.split('.')[1] == "txt":
            lvl = self.makeNewLevel(level)
            self.first_node = A_star(RHState(lvl), RHNode)
        else:
            print("unsupported input, give either a predefined level or a textfile as an argument")

    def makeNewLevel(self, level):
        result = []
        with open(level) as infile:
            for line in infile:
                result.append(tuple(map(int, line.split(','))))
        return result

    def solve(self):
        node, noGenerated, noExplored, explored = self.first_node.a_star_search()
        return node, noGenerated, noExplored, explored


s = RHSolver("rhboard/hard.txt")
node, noGenerated, noExplored, explored = s.solve()
print("Number of steps:", node.g_value, "\nNumber of nodes explored:", noExplored, "\nNumber of nodes generated:", noGenerated)
app = RHApp(explored, node.path())
app.mainloop()
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

    #Levels given in advance
    easy = [
            (0,2,2,2),
            (0,0,4,3),
            (0,3,4,2),
            (0,4,1,2),
            (1,2,0,2),
            (1,4,2,2)]
 
    medium = [
            (0,1,2,2),
            (0,0,5,3),
            (0,1,3,2),
            (0,3,0,2),
            (1,0,2,3),
            (1,2,0,2),
            (1,3,1,2),
            (1,3,3,3),
            (1,4,2,2),
            (1,5,0,2),
            (1,5,2,2)]

    hard = [
            (0,2,2,2),
            (0,0,4,2),
            (0,0,5,2),
            (0,2,5,2),
            (0,4,0,2),
            (1,0,0,3),
            (1,1,1,3),
            (1,2,0,2),
            (1,3,0,2),
            (1,4,2,2),
            (1,4,4,2),
            (1,5,3,3)]

    expert = [
            (0,0,2,2),
            (0,0,1,3),
            (0,0,5,2),
            (0,1,0,2),
            (0,2,3,2),
            (0,3,4,2),
            (1,0,3,2),
            (1,2,4,2),
            (1,3,0,3),
            (1,4,0,2),
            (1,4,2,2),
            (1,5,2,2),
            (1,5,4,2)]


s = RHSolver("easy")
node, noGenerated, noExplored, explored = s.solve()
print("Number of steps:", node.g_value, "\nNumber of nodes explored:", noExplored, "\nNumber of nodes generated:", noGenerated)
app = RHApp(explored, node.path())
app.mainloop()
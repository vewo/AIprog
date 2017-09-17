from Node import Node
from Node import State
from Node import Vehicle
from astar import A_star_search

#Importere data og gjøre om til vehicle object
#Lage start state med vehicle object
#Gi start state til Astar
#Får tilbake Goal-node der den har kommet til mål
#Backtracke fra goal-node for å finne path
#Backtack ferdig til parent node = start node

class Solver(object):
    board = ""
    results = []
    path = []

    def __init__(self, board):
        self.board = board
        with open(board) as infile:
            self.results = [[int(i) for i in line.strip().split(',')] for line in infile]

    def generateVehicleList(self):
        vehicleList = []
        number = -1
        for element in self.results:
            number += 1
            element.insert(0, number)
            listToTuple = tuple(element)
            vehicleList.append(Vehicle(*listToTuple))
        return vehicleList

    def generateStartState(self):
        start = State(self.generateVehicleList())
        return start

    def generateStartNode(self):
        startState = State(self.generateVehicleList())
        startNode = Node(startState, None)
        return startNode

    def findPath(self, goal):
        self.path.append(goal.parent)
        if (goal.parent != None):
            self.findPath(goal.parent)

s = Solver("easy.txt")
v = s.generateStartNode()
a = A_star_search(v)
print(a.a_star_search())
#s.findPath(g)
#print(len(s.path))
#print(s.path)



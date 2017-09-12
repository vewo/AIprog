import Node
from Node import State
from Node import Vehicle

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
        s = Solver("easy.txt")
        start = State(s.generateVehicleList)
        return start

    def findPath(self, goal):
        path.append(goal.getID)
        if (goal != start):
            findPath(goal.parent)

s = Solver("easy.txt")
s.generateVehicleList()

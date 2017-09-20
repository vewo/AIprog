

class Node():
    #Set initial parameters
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.g_value = 0
        if parent != None:
            self.g_value = self.parent.g_value + self.cost(parent)
        self.h_value = self.heuristic()
        self.f_value = self.h_value + self.g_value
        self.kids = []
    
    #Returns the path from the node to the start node. Used at the goal node
    #and returned reversed gives the path from the start node to the goal node
    def path(self): 
        path = []
        node = self
        while node != None:
            path.append(node)
            node = node.parent
        path.reverse()
        return path
    
    #Checks if the current node is a solution
    def isSolution(self):
        pass

    #Returns the cost from the parent to this node.
    def cost(self, parent):
        pass
    
    #Calculates the heuristic for the current node.
    def heuristic(self):
        pass
    
    #Creates the children of the current node.
    def createChildren(self):
        pass
    
    
class State():
    #Set initial parameters
    def __init__(self, state):
        self.state = self.initialize(state)
        self.ID = self.getID()
    
    #Initializes the state
    def initialize(self, state):
        pass
    
    #Gives the state a unique identifier
    def getID(self):
        pass

    #Represent the state in a format easy for visualization and computation
    def getGrid(self): 
        pass

    #Generate the possible states that can 
    def generateStates(self): 
        pass

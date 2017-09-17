

class Node():
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.g_value = 0
        if parent != 0:
            self.g_value = self.parent.g_value + self.cost(parent)
        self.h_value = self.heuristic()
        self.f_value = self.h_value + self.g_value
        self.kids = []
    
    def path(self): #Returns the path from the node to goal
        path = []
        node = self
        while node:
            path.append(node)
            node = node.parent
        return path.reverse()
    
    def isSolution(self):
        pass

    def cost(self, parent):
        pass
    
    def heuristic(self):
        pass
    
    def createChildren(self):
        pass
    
    
class State():
    def __init__(self, state):
        self.state = self.initialize(state)
        #print(self.state[0][0].segmentSizes)
        self.ID = self.getID()
        
    def initialize(self, state):
        pass
    
    def getID(self): #unique identifier for the state
        pass

    def getGrid(self): #represent state in format easy for visualization and computation
        pass

    def generateStates(self): #generate the possible states that can 
        pass

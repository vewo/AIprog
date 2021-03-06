import math
import copy

from General import Node, State

class RHNode(Node):
    #Initialize from superclass
    def __init__(self, state, parent):
        super(RHNode, self).__init__(state, parent)
            
    #Rush Hour specific cost for A*
    def cost(self, parent):
        return 1
    
    #Rush Hour specific heuristic for A*
    def heuristic(self):
        grid = self.state.getGrid() #get the grid
        target_car = self.state.state[0]
        no_blocks = 0
        goal_distance = 4 - target_car.x #the location of leftmost corner for car when in goal == 4
        
        #Check number of cars blocking between the target car and goal
        for x in range(target_car.x+target_car.size, 6): 
            if grid[x][2] != "x":
                no_blocks += 1
        return no_blocks + goal_distance

    #Rush Hour specific test to see if the node is a goal node
    def isSolution(self):
        return self.state.state[0].x == 4 #Check if leftmost corner of size 2 target car is in col 4 -> righmost corner in col 5 == goal

    #Rush Hour specific method for creating children
    def createChildren(self):
        feasible_states = self.state.generateStates()
        children = []
        for feasible_state in feasible_states:
            children.append(RHNode(feasible_state, self))
        return children

class RHState(State):
    #Initialize from superclass
    def __init__(self, state):
        super(RHState, self).__init__(state)
    
    ##Rush Hour specific initialization method
    def initialize(self, state):
        vehicles = []
        no = 0
        for line in state:
            vehicles.append(Vehicle(no, *line)) #unpacking tuple into arguments for Vehicle class __init__ method
            no += 1
        return vehicles
    
    #Returns a unique identifier for the state
    def getID(self):
        return hash(''.join(str(e) for e in self.getGrid()))
    
    #Returns the grid with vehicle objects
    def getGrid(self):
        grid = [["x" for column in range(6)] for row in range(6)]
        #Adding vehicles to the grid
        for v in self.state:
            if v.orientation == 0:   #horizontal
                for x in range(v.size):
                    grid[v.x + x][v.y] = v.no
            else:  #vertical
                for y in range(v.size):
                    grid[v.x][v.y + y] = v.no
        return grid

    #Creates a state with a list of vehicles as input
    def makeState(self, vehicles):
        state = []
        #Adds the quad to the state
        for v in vehicles:
            state.append(v.getTuple())
        new_state = RHState(state)
        return new_state
    
    #Generates feasible states
    def generateStates(self): 
        grid = self.getGrid()
        feasible_states = []
        
        for v in self.state:
            if v.orientation == 0: #horizontal orientation
                left = v.x #x-coordinate of leftmost part of the vehicle
                right = v.x+v.size-1 #x-coordinate of rightmost part of the vehicle
                y = v.y #y-coordinate of the vehicle
                       
                if(left != 0 and grid[left - 1][y] == "x"): #the vehicle can move to the left       
                    vehicles = copy.deepcopy(self.state) #list of vehicles to be used to generate states
                    vehicles[v.no].x -= 1
                    feasible_states.append(self.makeState(vehicles))
            
                if(right != 5 and grid[right + 1][y] == "x"): #the vehicle can move to the right
                    vehicles = copy.deepcopy(self.state) #list of vehicles to be used to generate states
                    vehicles[v.no].x += 1
                    feasible_states.append(self.makeState(vehicles))

            else: #vertical orientation
                top = v.y #y-coordinate of top part of the vehicle
                bottom = v.y+v.size-1 #y-coordinate of bottom part of the vehicle
                x = v.x #x-coordinate of the vehicle

                if(top != 0 and grid[x][top - 1] == "x"): #the vehicle can move up
                    vehicles = copy.deepcopy(self.state) #list of vehicles to be used to generate states
                    vehicles[v.no].y -= 1
                    feasible_states.append(self.makeState(vehicles))
                
                if(bottom != 5 and grid[x][bottom + 1] == "x"): #the vehicle can move down
                    vehicles = copy.deepcopy(self.state) #list of vehicles to be used to generate states
                    vehicles[v.no].y += 1
                    feasible_states.append(self.makeState(vehicles))

        return feasible_states

class Vehicle():
    #Initialize
    def __init__(self, no, orientation, x, y, size):
        self.no = no
        self.orientation = orientation
        self.x = x
        self.y = y
        self.size = size
    #Returns the quad of a vehicle.
    def getTuple(self):
        return (self.orientation, self.x, self.y, self.size)

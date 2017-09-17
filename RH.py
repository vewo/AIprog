import time
import math
import copy

from AStar import A_star
from General import Node
from General import State



class RHNode(Node):
    def __init__(self, state, parent):
        super(RHNode, self).__init__(state, parent)
            
    def cost(self, parent):
        return 1
    
    def heuristic(self):
        grid = self.state.getGrid() #get the grid
        target_car = self.state.state[0]
        no_blocks = 0
        goal_distance = 4 - target_car.x #the location of leftmost corner for car when in goal == 4
        for x in range(target_car.x+target_car.size, 6): #check number of cars blocking between the target car and goal
            if grid[x][2] != "x":
                no_blocks += 1
        return no_blocks + goal_distance

    def isSolution(self):
        return self.state.state[0].x == 4 #Check if leftmost corner of size 2 target car is in col 4 -> righmost corner in col 5 == goal

    def createChildren(self):
        feasible_states = self.state.generateStates()
        children = []
        for feasible_state in feasible_states:
            children.append(RHNode(feasible_state, self))
        return children

class RHState(State):
    def __init__(self, state):
        super(RHState, self).__init__(state)
    
    def initialize(self, state):
        vehicles = []
        no = 0
        for line in state:
            vehicles.append(Vehicle(no, *line)) #unpacking tuple into arguments for Vehicle class __init__ method
            no += 1
        return vehicles
    
    def getID(self): #unique identifier for the state
        return hash(''.join(str(e) for e in self.getGrid()))
    
    def getGrid(self):
        grid = [["x" for column in range(6)] for row in range(6)]
        for v in self.state: #adding vehicles to the grid
            if v.orientation == 0:   #horizontal
                for x in range(v.size):
                    grid[v.x + x][v.y] = v.no
            else:  #vertical
                for y in range(v.size):
                    grid[v.x][v.y + y] = v.no
        return grid

    def makeState(self, vehicles):
        state = []
        for v in vehicles:
            state.append(v.getTuple())
        new_state = RHState(state)
        return new_state
          
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
    def __init__(self, no, orientation, x, y, size):
        self.no = no
        self.orientation = orientation
        self.x = x
        self.y = y
        self.size = size
    
    def getTuple(self):
        return (self.orientation, self.x, self.y, self.size)

class Solver():

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
        node, generated, explored = self.first_node.a_star_search()
        return node, generated, explored

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


s = Solver("hard")
node, generated, explored = s.solve()
print(node.g_value)
print(explored)
print(generated)


'''
    start_time = time.clock()

    print("Solving easy")
    first_node = A_star(RHState(easy), RHNode)
    node, generated, explored = first_node.a_star_search()
    print("Number of steps:", node.g_value, "Number of nodes considered:", explored, "Number of nodes generated:", generated)

    print(time.clock() - start_time, "seconds")
    start_time = time.clock()

    print("Solving medium")
    first_node = A_star(RHState(medium), RHNode)
    node, generated, explored = first_node.a_star_search()
    print("Number of steps:", node.g_value, "Number of nodes considered:", explored, "Number of nodes generated:", generated)

    print(time.clock() - start_time, "seconds")
    start_time = time.clock()

    print("Solving hard")
    first_node = A_star(RHState(hard), RHNode)
    node, generated, explored = first_node.a_star_search()
    print("Number of steps:", node.g_value, "Number of nodes considered:", explored, "Number of nodes generated:", generated)

    print(time.clock() - start_time, "seconds")
    start_time = time.clock()

    print("Solving expert")
    first_node = A_star(RHState(expert), RHNode)
    node, generated, explored = first_node.a_star_search()
    print("Number of steps:", node.g_value, "Number of nodes considered:", explored, "Number of nodes generated:", generated)

    print(time.clock() - start_time, "seconds")
'''

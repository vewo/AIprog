import time
import math
import copy

from v2 import A_star
from v2 import Node
from v2 import State



class RHNode(Node):
    def __init__(self, state, parent):
        super(RHNode, self).__init__(state, parent)
            
    def cost(self, parent):
        return 1
    
    def heuristic(self):
        grid = self.state.getState() #get the grid
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
        possible_states = self.state.generateStates()
        children = []
        for possible_state in possible_states:
            children.append(RHNode(possible_state, self))
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
        return hash(''.join(str(e) for e in self.getState()))
    
    def getState(self):
        grid = [["x" for column in range(6)] for row in range(6)]
        for v in self.state: #adding vehicles to the board
            if v.orientation == 0:   #horizontal
                for x in range(v.size):
                    grid[v.x + x][v.y] = v.no
            else:  #vertical
                for y in range(v.size):
                    grid[v.x][v.y + y] = v.no
        return grid

    def createStateObject(self, vehicles):
        state = []
        for v in vehicles:
            state.append(v.toTuple())
            new_state = RHState(state)
        return new_state
          
    def generateStates(self): 
        board = self.getState()
        possible_states = []
        
        for v in self.state:
            #Horizontal orientation of vehicle
            if v.orientation == 0:
                left_most = v.getLocation()[0]
                right_most = v.getLocation()[-1]
                       
                if(left_most[0] != 0 and board[left_most[0] - 1][left_most[1]] == "x"):        
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.no].x -= 1
                    possible_states.append(self.createStateObject(temp_vehicles))
            
                if(right_most[0] != 5 and board[right_most[0] + 1][right_most[1]] == "x"):
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.no].x += 1
                    possible_states.append(self.createStateObject(temp_vehicles))
                
            #Vertical orientation of vehicle
            else:
                top = v.getLocation()[0]
                bottom = v.getLocation()[-1]

                if(top[1] != 0 and board[top[0]][top[1] - 1] == "x"):
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.no].y -= 1

                    possible_states.append(self.createStateObject(temp_vehicles))
                
                if(bottom[1] != 5 and board[bottom[0]][bottom[1] + 1] == "x"):
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.no].y += 1

                    possible_states.append(self.createStateObject(temp_vehicles))
        return possible_states

class Vehicle():
    def __init__(self, no, orientation, x, y, size):
        self.no = no
        self.orientation = orientation
        self.x = x
        self.y = y
        self.size = size
    
    #Return the location of the vehicle (tuples with (x and y coordinates))
    def getLocation(self):
        location = []
        #Horizontal orientation of vehicle
        if self.orientation == 0:
            for i in range(self.size):
                location.append((self.x + i, self.y))
        #Vertical orientation of vehicle
        if self.orientation == 1:
            for i in range(self.size):
                location.append((self.x, self.y + i))
        return location
    
    def toTuple(self):
        return (self.orientation, self.x, self.y, self.size)

class Solver():

    def __init__(self, level):
        if level == easy:
            first_node = A_star(RHState(easy), RHNode)
        if level == medium:
            first_node = A_star(RHState(medium), RHNode)
        if level == hard:
            first_node = A_star(RHState(hard), RHNode)
        if level == expert:
            first_node = A_star(RHState(expert), RHNode)
        if level.split('.')[1] == "txt":
            first_node = A_star(RHState(makeNewLevel(level)), RHNode)

    def makeNewLevel(self, level):
        level = []
        with open(level) as infile:
            self.level = ['(', line, ')'] for line in infile]




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

start_time = time.clock()


print("Solving easy")
first_node = A_star(RHState(easy), RHNode)
node, generated, explored = first_node.a_star_search()
print("Number of steps:", node.g_value, "Number of nodes considered:", explored, "Number of nodes generated:", generated)

print(time.clock() - start_time, "seconds")
start_time = time.clock()

print("Solving medium")
first_node = A_star(RHState(easy), RHNode)
node, generated, explored = first_node.a_star_search()
print("Number of steps:", node.g_value, "Number of nodes considered:", explored, "Number of nodes generated:", generated)

print(time.clock() - start_time, "seconds")
start_time = time.clock()

print("Solving hard")
first_node = A_star(RHState(easy), RHNode)
node, generated, explored = first_node.a_star_search()
print("Number of steps:", node.g_value, "Number of nodes considered:", explored, "Number of nodes generated:", generated)

print(time.clock() - start_time, "seconds")
start_time = time.clock()

print("Solving expert")
first_node = A_star(RHState(easy), RHNode)
node, generated, explored = first_node.a_star_search()
print("Number of steps:", node.g_value, "Number of nodes considered:", explored, "Number of nodes generated:", generated)

print(time.clock() - start_time, "seconds")

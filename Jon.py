from queue import PriorityQueue
import copy

class AStar:
    def __init__(self, start):
        self.start = start
        self.open_nodes = []
        self.open_values = []
        self.explored = set()
        self.count = 1
    
    def checkState(self, state):
        for n in range(0, len(self.open_nodes)):
            if self.open_nodes[n].state.getStateId() == state.getStateId():
                return n
        return False
        
    def putNode(self, node):
        self.open_nodes.append(node)
        self.open_values.append(node.f)
    
    def popNode(self):
        smallest = self.open_values[0]
        smallest_index = 0
        for n in range(0, len(self.open_values)):
            if self.open_values[n] < smallest:
                smallest = self.open_values[n]
                smallest_index = n
        temp_node = self.open_nodes[smallest_index]
        del self.open_nodes[smallest_index]
        del self.open_values[smallest_index]
        return temp_node
    
    def deleteNode(self, node):
        index = self.open_nodes(node)
        print("sletter node")
        del self.open_nodes[index]
        del self.open_values[index]
        
    def solve(self):       
        init_node = RushHourNode(self.start, 0)
        
        #Checking if first node is a solution
        if(init_node.isSolution()):
            return init_node, self.count
        
        self.putNode(init_node)
        
        #as long as open_nodes is not empty
        while(self.open_nodes):
            temp_node = self.popNode()
            #Counting number of nodes considered
            self.count += 1
            
            #If solution is found
            if(temp_node.isSolution()):
                return temp_node, self.count
            
            self.explored.add(temp_node.state.getStateId())
            for child in temp_node.createChildren():   
                child_node = RushHourNode(child, temp_node)
                if child.getStateId() not in self.explored and not self.checkState(child):
                    self.putNode(child_node)
                elif self.checkState(child):
                    incumbent = self.open_nodes[self.checkState(child)]
                    #print("sammenligner incumbent", incumbent.f, "med child node f value", child_node.f)
                    if child_node.f < incumbent.f:

                        print("fant bedre node")
                        self.deleteNode(incumbent)
                        self.putNode(child_node)

        return None

class RushHourNode(object):
    def __init__(self, state, parent=None):
        self.state = state #board object
        self.parent = parent
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
        self.f = self.depth + self.computeH()
            
    #Problem specific classes
    def computeH(self):
        board = self.state.getState()
        num_blocks = 0
        distance = abs(5 - self.state.state[0].getCoordinates()[-1][0])
        for n in range(5, 0, -1):
            if board[n][2] == 0:
                break
            if board[n][2] != ".":
                num_blocks += 1
        return (num_blocks*0.5 + distance*0.5)/4
    
    def createChildren(self):
        return self.state.generateStates()

    def isSolution(self):
        return self.state.state[0].getCoordinates()[-1] == (5, 2) 
    
    #Letting PriorityQeueue compare on another value than F if F is the same for both nodes
    def __lt__(self, node):
        return hash(self.state) < hash(node.state)
    
    def __eq__(self, other):
        return isinstance(other, RushHourNode) and self.state.getStateId() == other.state.getStateId()
    
    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    
class SearchState(object):
    def __init__(self, input_string):
        self.state = self.initState(input_string)
        
    def initState(self, input_string):
        pass
    
    def getStateId(self): #create-state-identifier
        pass

    def getState(self): #visualize the state
        pass

    def printState(self): #visualize the state
        pass
    
    def generateStates(self): #
        pass

    
class RushHourSearchState(SearchState):
    def __init__(self, input_string):
        super(RushHourSearchState, self).__init__(input_string)
    
    def initState(self, input_string):
        vehicles = []
        num = 0
        for line in input_string:
            vehicles.append(Vehicle(num, *line))
            num += 1
        
        return vehicles
    
    def getStateId(self): #create-state-identifier
        return hash(''.join(str(e) for e in self.getState()))
    
    def getState(self):
        board = [["." for x in range(6)] for y in range(6)]
    
        #Adding vehicles
        for v in self.state:
            #Horizontal orientation of vehicle
            if v.o == 0:
                for y in range(v.s):
                    board[v.x + y][v.y] = v.num
            #Vertical orientation of vehicle
            else:
                for x in range(v.s):
                    board[v.x][v.y + x] = v.num
        return board

    def generateBoard(self, vehicles):
        board = [["." for x in range(6)] for y in range(6)]
    
        #Adding vehicles
        for v in vehicles:
            #Horizontal orientation of vehicle
            if v.o == 0:
                for y in range(v.s):
                    board[v.x + y][v.y] = v.num
            #Vertical orientation of vehicle
            else:
                for x in range(v.s):
                    board[v.x][v.y + x] = v.num
        
        return board
    
    def printState(self):
        board = self.getState()
        for y in range(len(board)):
            for x in range(len(board[y])):
                print(str(board[x][y]), end='  ')
            print('\n')
    
    def createStateObject(self, vehicles):
        temp_state = []
        for v in vehicles:
            temp_state.append(v.toTuple())
            new_state = RushHourSearchState(temp_state)
        return new_state
          
    def generateStates(self): 
        board = self.getState()
        possible_states = []
        
        for v in self.state:
            #Horizontal orientation of vehicle
            if v.o == 0:
                left_most = v.getCoordinates()[0]
                right_most = v.getCoordinates()[-1]
                       
                if(left_most[0] != 0 and board[left_most[0] - 1][left_most[1]] == '.'):        
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.num].x -= 1
                    possible_states.append(self.createStateObject(temp_vehicles))
            
                if(right_most[0] != 5 and board[right_most[0] + 1][right_most[1]] == '.'):
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.num].x += 1
                    possible_states.append(self.createStateObject(temp_vehicles))
                
        #Vertical orientation of vehicle
            else:
                top = v.getCoordinates()[0]
                bottom = v.getCoordinates()[-1]

                if(top[1] != 0 and board[top[0]][top[1] - 1] == '.'):
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.num].y -= 1

                    possible_states.append(self.createStateObject(temp_vehicles))
                
                if(bottom[1] != 5 and board[bottom[0]][bottom[1] + 1] == '.'):
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.num].y += 1

                    possible_states.append(self.createStateObject(temp_vehicles))
        return possible_states

class Vehicle:
    def __init__(self, num, o, x, y, s):
        self.num = num
        self.o = o #orientation (0 for horizontal, 1 for vertical)
        self.x = x #x-coordinate
        self.y = y #y-coordinate
        self.s = s #size
    
    #Return the coordinates (tuples with (x and y values)) of the squares that the vehicle covers
    def getCoordinates(self):
        coordinates = []
        #Horizontal orientation of vehicle
        if self.o == 0:
            for i in range(self.s):
                coordinates.append((self.x + i, self.y))
        #Vertical orientation of vehicle
        if self.o == 1:
            for i in range(self.s):
                coordinates.append((self.x, self.y + i))
        return coordinates
    
    def toTuple(self):
        return (self.o, self.x, self.y, self.s)

EASY = [
        (0,2,2,2),
        (0,0,4,3),
        (0,3,4,2),
        (0,4,1,2),
        (1,2,0,2),
        (1,4,2,2)]
 
MEDIUM = [
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
            (1,5,2,2)
]

HARD = [
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
    (1,5,3,3)
]

EXPERT = [
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
    (1,5,4,2)
]

print("Solving easy")
first_node = AStar(RushHourSearchState(EASY))
node, count = first_node.solve()
print(node.depth, count)

print("Solving medium")
first_node = AStar(RushHourSearchState(MEDIUM))
node, count = first_node.solve()
print(node.depth, count)

print("Solving hard")
first_node = AStar(RushHourSearchState(HARD))
node, count = first_node.solve()
print(node.depth, count)

print("Solving expert")
first_node = AStar(RushHourSearchState(EXPERT))
node, count = first_node.solve()
print(node.depth, count)
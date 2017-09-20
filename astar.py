
class A_star():
    
    def __init__(self, start, nodemode):
        self.start = start #sets the start state
        self.frontier_f_values = [] # the f values of the nodes in frontier, on same index as the respective node
        self.frontier = [] # the open nodes
        self.closed = set() # ID of closed nodes, should not allow for duplicates
        self.explored = 0 #to measure the no of nodes the search explores
        self.explored_nodes = []
        self.generated = 0 #to measure the no of nodes the search generates
        self.nodemode = nodemode # to generalize to different kinds of problems
    
    #If the state already exists, returns the index in frontier of the node with that state. If the state doesn't exist, returns false.
    def existingState(self, state):
        dict = {}
        for i in range(len(self.frontier)): #Make dictionary of generated states and their respective nodes' index in frontier
            dict[self.frontier[i].state.getID()] = i 
        if state.getID() in dict:
            return dict.get(state.getID()) #returns index (in frontier) of potentially created node
        return False

    #Functions for managing the lists of open nodes and their respective f_values

    #Inserts in frontier
    def put(self, node):
        self.frontier_f_values.append(node.f_value)
        self.frontier.append(node)
    
    #Returns the best option from frontier, and removes it
    def get(self):
        lowest = self.frontier_f_values.index(min(self.frontier_f_values)) #Find smallest f_value of open nodes
        best_option = self.frontier[lowest]
        del self.frontier_f_values[lowest]
        del self.frontier[lowest]
        return best_option

        #bfs = self.frontier[0]
        #del self.frontier[0]
        #return bfs

        #dfs = self.frontier[-1]
        #del self.frontier[-1]
        #return dfs
        
        
    #Removes a node from frontier
    def remove(self, node_index):
        del self.frontier_f_values[node_index]
        del self.frontier[node_index]
    
    #The general A* code.
    def a_star_search(self):
        #Make first start state into problem specific node and put it into frontier.
        first = self.nodemode(self.start, None)
        self.generated += 1
        self.put(first)
        
        #As long as frontier is not empty, pop item from frontier, add the state to closed and the node to explored. Check if current node is a
        #solution, if not, generate children. If a child is not in closed and its state doesn't exist from before, put it in frontier. If the
        #state exists from before, check if the child node has a lower cost than the previous explored node.
        while(self.frontier):
            x = self.get()
            self.explored += 1
            self.closed.add(x.state.getID())
            self.explored_nodes.append(x)
            if(x.isSolution()): #check if x is solution
                return x, self.generated, self.explored, self.explored_nodes
            
            childNodes = x.createChildren()
            self.generated += len(childNodes)
            for child in childNodes: #list of child-nodes
                existing = self.existingState(child.state) #check if node with same state is in frontier, if so returns it's index in the frontier
                if child.state.getID() not in self.closed and not existing:
                    self.put(child)
                elif existing:
                    old = self.frontier[existing]
                    if child.g_value < old.g_value: #Means one has found a cheaper way to get to the same state, as the heuristic will be equal
                        self.remove(existing)
                        self.put(child)
        return False


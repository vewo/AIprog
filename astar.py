
class A_star():
    
    def __init__(self, start, nodemode):
        self.start = start #sets the start state
        self.frontier_f_values = [] # the f values of the nodes in frontier, on same index as the respective node
        self.frontier = [] # the open nodes
        self.closed = set() # closed nodes, should not allow for duplicates
        self.explored = 0 #to measure the no of nodes the search explores
        self.generated = 0 #to measure the no of nodes the search generates
        self.nodemode = nodemode # to generalize to different kinds of problems
    
    def existingState(self, state):
        dict = {}
        for i in range(len(self.frontier)): #Make dictionary of generated states and their respective nodes' index in frontier
            dict[self.frontier[i].state.ID] = i 
        if state.ID in dict:
            return dict.get(state.ID) #returns index (in frontier) of potentially created node
        return False

    #Functions for managing the lists of open nodes and their respective f_values   
    def put(self, node):
        self.frontier_f_values.append(node.f_value)
        self.frontier.append(node)
    
    def get(self):
        lowest = self.frontier_f_values.index(min(self.frontier_f_values)) #Find smallest f_value of open nodes
        best_option = self.frontier[lowest]
        del self.frontier_f_values[lowest]
        del self.frontier[lowest]
        return best_option
    
    def remove(self, node_index):
        del self.frontier_f_values[node_index]
        del self.frontier[node_index]
        
    def a_star_search(self):
        #Make first start state into problem specific node
        first = self.nodemode(self.start, 0)
        self.generated += 1
        self.put(first)
        
        #as long as frontier is not empty
        while(self.frontier):
            x = self.get()
            self.explored += 1
            self.closed.add(x.state.getID())
            
            if(x.isSolution()): #check if x is solution
                return x, self.generated, self.explored
            
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
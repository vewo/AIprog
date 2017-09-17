    def generateBoard(self, vehicles):
        print("Brukes nå")
        board = [["." for x in range(6)] for y in range(6)]
    
        #Adding vehicles
        for v in vehicles:
            #Horizontal orientation of vehicle
            if v.orientation == 0:
                for y in range(v.size):
                    board[v.x + y][v.y] = v.no
            #Vertical orientation of vehicle
            else:
                for x in range(v.size):
                    board[v.x][v.y + x] = v.no
        
        return board


    def printState(self):
        grid = self.getState()
        for y in range(len(board)):
            for x in range(len(board[y])):
                print(str(board[x][y]), end='  ')
            print('\n')


            else: #vertical orientation
                top = v.getLocation()[0]
                bottom = v.getLocation()[-1]

                if(top[1] != 0 and grid[top[0]][top[1] - 1] == "x"):
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.no].y -= 1

                    possible_states.append(self.makeState(temp_vehicles))
                
                if(bottom[1] != 5 and grid[bottom[0]][bottom[1] + 1] == "x"):
                    temp_vehicles = copy.deepcopy(self.state) #temp list for vehicles to generate states from
                    temp_vehicles[v.no].y += 1

                    possible_states.append(self.makeState(temp_vehicles))
        return possible_states

    def getLocation(self): #return the location of the vehicle (tuples with x and y coordinates)
        location = []
        #Horizontal
        if self.orientation == 0:
            for x in range(self.size):
                location.append((self.x + x, self.y))
        #Vertical
        if self.orientation == 1:
            for y in range(self.size):
                location.append((self.x, self.y + y))
        return location



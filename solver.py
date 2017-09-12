from Node import Vehicle

#Importere data og gjøre om til vehicle object
#Lage start state med vehicle object
#Gi start state til Astar
#Får tilbake Goal-node der den har kommet til mål
#Backtracke fra goal-node for å finne path
#Backtack ferdig til parent node = start node

vehicleList = []

E = [[0,2,2,2],
[0,0,4,3],
[0,3,4,2],
[0,4,1,2],
[1,2,0,2],
[1,4,2,2]]

def generateVehicleList(Board):
    number = -1
    for element in Board:
        number += 1
        element.append(number)
        listToTuple = tuple(element)
        vehicleList.append(Vehicle(*listToTuple))

generateVehicleList(E)

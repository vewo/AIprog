from Node import Vehicle

#Importere data og gjøre om til vehicle object
#Lage start state med vehicle object
#Gi start state til Astar
#Får tilbake Goal-node der den har kommet til mål
#Backtracke fra goal-node for å finne path
#Backtack ferdig til parent node = start node

results = []
with open('easy.txt') as infile:
    results = [[int(i) for i in line.strip().split(',')] for line in infile]

def generateVehicleList(Board):
    vehicleList = []
    number = -1
    for element in Board:
        number += 1
        element.append(number)
        listToTuple = tuple(element)
        vehicleList.append(Vehicle(*listToTuple))
    return vehicleList

generateVehicleList(results)

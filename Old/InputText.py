


easy = [
        (0,2,2,2),
        (0,0,4,3),
        (0,3,4,2),
        (0,4,1,2),
        (1,2,0,2),
        (1,4,2,2)]

def makeNewLevel(level):
        result = []
        with open(level) as infile:
        	for line in infile:
        		result.append(tuple(map(int, line.split(','))))
        return result




print(easy)
k = makeNewLevel("easy.txt")
print(k)
print(easy == k)
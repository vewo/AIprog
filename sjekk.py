




def makeNewLevel(level):
        rows = []
        columns = []
        with open(level) as infile:
        	firstLine = infile.readline().split(' ')
        	noCols = int(firstLine[0])
        	noRows = int(firstLine[1])
        	for i in range(noRows):
        		rowLine = infile.readline().strip("\n").split(" ")
        		row = []
        		for ss in rowLine: 
        			row.append(int(ss))
        		rows.append(row)
        	for i in range(noCols):
        		colLine = infile.readline().strip("\n").split(" ")
        		col = []
        		for ss in colLine: 
        			col.append(int(ss))
        		columns.append(col)
        return [rows, columns]


print(makeNewLevel("cat.txt"))
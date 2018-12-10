file = '../inputs/day6.txt'
sample = '../inputs/sample.txt';

max = 10000

#returns (x,y) from a given input line
def getCoordinate(line):
	return list(map(int,line.split(',')))

#get the dimensions of the graph by finding the largest X and Y values
def dimensions(coordinates):
	maxX,maxY = [0,0]
	for coor in coordinates:
		x,y = getCoordinate(coor)
		maxX = x if x > maxX else maxX
		maxY = y if y > maxY else maxY
	return (maxX,maxY)

#builds the grid where each coorindate has a [value,[ids]] list
def buildGrid(x,y,initialValue):
	grid = []
	for i in range(0,x+1):
		column = []
		for i in range(0,y+1):
			column.append([initialValue,[]])
		grid.append(column)
	return grid

# adds each of the coordinates and runs a function on the grid on each iteration accordingly
def addPoints(grid,coordinates,addFunc):
	id = 0
	for coor in coordinates:
		addFunc(grid,getCoordinate(coor),id)
		id += 1

# adds a given point and iterates through the grid to redefine the manhattan distances
def addPoint(grid,coor,id):
	x,y = coor
	grid[x][y] = [0,[id]]
	num = findClosest(grid,coor,id)

#updates the manhattan distances on the map
def findClosest(grid,coor,id):
	x,y = coor
	for i in range(0,len(grid)):
		for j in range(0,len(grid[i])):
			closest,points = grid[i][j]
			distance = abs(x-i) + abs(y-j)
			if closest == 0:
				continue
			elif closest > distance or closest == -1:
				closest = distance
				points = [id]
				grid[i][j] = distance
			elif closest == distance:
				points.append(id)
			grid[i][j] = [closest,points]

#finds the manhattan areas, removes the ones that are infinite, and returns the largest one
def findLargestArea(grid):
	areaList = {}
	for columns in grid:
		for entry in columns:
			distance,points = entry
			if len(points) == 1:
				id = points[0]
				if id in areaList:
					areaList[id] += 1
				else:
					areaList[id] = 1
	filterCorners(grid,areaList)
	return maxArea(areaList)

#max function
def maxArea(areaList):
	max = 0
	for k in areaList.keys():
		max = areaList[k]  if areaList[k]> max else max
	return max 

#if an id touches a corner, it is an infinite sized map, so we remove it
def filterCorners(grid,areaList):
	for y in range(0,len(grid[0])):
		removeEntry(areaList,grid[0][y][1])
		removeEntry(areaList,grid[len(grid)-1][y][1])
	for x in range(0,len(grid)):
		removeEntry(areaList,grid[x][0][1])
		removeEntry(areaList,grid[x][len(grid[x])-1][1])

#remove entry from the map
def removeEntry(areaList,points):
	if len(points) == 1:
		areaList[points[0]] = 0

#adds the id to the point and adds the manhattan sum to each of the points in the grid
def appendPoint(grid,coor,id):
	x,y = coor
	grid[x][y][1].append(id)
	num = appendScores(grid,coor,id)

#at each coordinate, add the manhattan sum to the grid
def appendScores(grid,coor,id):
	x,y = coor
	for i in range(0,len(grid)):
		for j in range(0,len(grid[i])):
			closest,points = grid[i][j]
			if closest == -1:
				continue
			distance = abs(x-i) + abs(y-j)
			closest += distance
			if closest >= max:
				closest = -1
			else:
				points.append(id)
			grid[i][j] = [closest,points]

#count the number of spaces that have valid total distances
def countSpace(grid):
	sum = 0
	for column in grid:
		for entry in column:
			sum += 1 if entry[0] != -1 else 0
	return sum 


if __name__ == '__main__':
	coordinates = open(file,'r').readlines()
	# coordinates = open(sample,'r').readlines()

	# part1
	grid = buildGrid(*dimensions(coordinates),-1)
	addPoints(grid,coordinates,addPoint)
	print(findLargestArea(grid))
	# part2
	grid = buildGrid(*dimensions(coordinates),0)
	addPoints(grid,coordinates,appendPoint)
	print(countSpace(grid))


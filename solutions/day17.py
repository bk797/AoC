file = '../inputs/day17.txt'
sample = '../inputs/sample.txt'

class Reservoir:

	def __init__(self,grid,spring):
		self.grid = grid
		self.spring = spring
		self.grid[spring[0]][spring[1]] = '+'

	#fill horizontally until meet a wall
	#assume that when the necessary checks were made before running the method
	# ie blocks underneath are all # or ~
	def fillHorizontal(self,x,y):
		self.grid[x][y] = '~'
		rY = y+1
		while self.grid[x][rY] != '#':
			self.grid[x][rY] = '~'
			rY += 1
		lY = y-1
		while self.grid[x][lY] != '#':
			self.grid[x][lY] = '~'
			lY -= 1

	#flow startring from the spring block
	def flowSpring(self):
		sX,sY = self.spring
		self.flow(sX+1,sY)

	'''
		function that deals with the flowing of the water
		1) go as far down as possible
		2) while going back up, 
		  a) fill horizontally if possible
		  b) if not, if on top of ~ of #, try to propogate sideways
		  c) if underneath a |, just turn into a |
	'''
	def flow(self,x,y):
		if self.grid[x][y] not in '#~|':
			self.grid[x][y] == '|'
			maxX = x
			while (maxX+1) < len(self.grid) and self.grid[maxX+1][y] == '.':
				maxX += 1
			while maxX >= x:
				if self.canFill(maxX,y):
					self.fillHorizontal(maxX,y)
					maxX -= 1
				else:
					self.grid[maxX][y] = '|'
					if (maxX+1) != len(self.grid) and self.grid[maxX+1][y] is not '|':
						rY = y+1
						while self.grid[maxX+1][rY] in '~#' and self.grid[maxX][rY] not in '~#|':
							self.grid[maxX][rY] = '|'
							rY += 1
						if self.grid[maxX][rY] == '.':
							self.flow(maxX,rY)
						lY = y-1
						while self.grid[maxX+1][lY] in '~#' and self.grid[maxX][lY] not in '~#|':
							self.grid[maxX][lY] = '|'
							lY -= 1
						if self.grid[maxX][lY] == '.':
							self.flow(maxX,lY)
					maxX -= 1

	# checks if it is possilbe to fill horizontally with water
	# checks if surrounded by # and has # or ~ underneath
	def canFill(self,x,y):
		if self.grid[x][y] != '.':
			return False
		try:
			rY = y+1
			while self.grid[x][rY] != '#':
				if self.grid[x+1][rY] == '.':
					return False
				rY += 1
			lY = y - 1
			while self.grid[x][lY] != '#':
				if self.grid[x+1][lY] == '.':
					return False
				lY -= 1
			return True
		except:
			return False

	#counts total water tiles 
	def countWater(self):
		totalWater= 0
		tiles = 0
		for row in self.grid:
			for char in row:
				if char == '~':
					totalWater += 1
					tiles += 1
				elif char == '|':
					totalWater += 1
		return (totalWater,tiles)

	def __str__(self):
		string = ''
		for row in self.grid:
			string += ''.join(row)+ '\n'
		return string
# reads input to build coordinates
def getCoordinates(lines):
	points = []
	for line in lines:
		if line[0] == 'x':
			x,y = line.split(',')
			x = int(x.split('=')[1])
			y0,y1 = y.split('=')[1].split('..')
			y0 = int(y0)
			y1 = int(y1)
			for y in range(y0,y1+1):
				points.append((y,x))
		else:
			y,x = line.split(',')
			y = int(y.split('=')[1])
			x0,x1 = x.split('=')[1].split('..')
			x0 = int(x0)
			x1 = int(x1)
			for x in range(x0,x1+1):
				points.append((y,x))
	points.sort()
	return points

#find minX and maxX
def xRange(points):
	points.sort(key=lambda x: x[0],reverse=False)
	return (points[0][0],points[len(points)-1][0])

#find minY and mxY
def yRange(points):
	points.sort(key=lambda x: x[1],reverse = False)
	return (points[0][1],points[len(points)-1][1])

#build the reservoir with the given points
def buildReservoir(points):
	minX,maxX = xRange(points)
	minY,maxY = yRange(points)
	grid = []
	for i in range(-1,maxX-minX+1):
		grid.append(['.' for i in range(0,maxY-minY+1)])
	for point in points:
		x,y = point
		grid[x-minX+1][y-minY] = '#'
	return Reservoir(grid,(0,500-minY))

if __name__ == '__main__':
	lines = open(file,'r').readlines()
	points = getCoordinates(lines)
	grid = buildReservoir(points)
	grid.flowSpring()
	print("part1","part2")
	print(grid.countWater())

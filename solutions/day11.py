var_serial = 9798
var_bounds = 300

def powerLevel(x,y,serial):
	rackId = x+10
	pl = (rackId * y + serial) * rackId
	return int(str(pl)[-3]) - 5

class Grid:

	def __init__(self,bounds,serial):
		self.grid = []
		self.serial = serial
		self.bounds = bounds
		self.buildGrid()

	def buildGrid(self):
		bounds = self.bounds
		serial = self.serial
		for x in range(0,bounds):
			col = []
			for y in range(0,bounds):
				col.append(powerLevel(x,y,serial))
			self.grid.append(col)

	def getSumGrid(self,size):
		bounds = self.bounds
		sumGrid = []
		for x in range(0,bounds-size):
			col = []
			for y in range(0,bounds-size):
				sum = 0
				for yd in range(y,y+size):
					sum += self.grid[x][yd]
				col.append(sum)
			sumGrid.append(col)
		return sumGrid

def largestGrid(sumGrid,size):
	bounds = len(sumGrid)
	max = 0
	maxX = -1
	maxY = -1
	for y in range(0,bounds-size):
		for x in range(0,bounds-size):
			sum = 0
			for dx in range(x,x+size):
				sum += sumGrid[dx][y]
			if sum > max:
				maxX = x
				maxY = y
				max = sum
	return [maxX,maxY,max]

def largestSquare(grid):
	bounds = grid.bounds
	max = 0
	x,y,b = [-1,-1,-1]
	for i in range(1,bounds+1):
		tx,ty,m = largestGrid(grid.getSumGrid(i),i)
		if m > max:
			x = tx
			y = ty
			b = i
			max = m 
	return [x,y,b]

if __name__ == '__main__':
	grid = Grid(var_bounds,var_serial)
	# print(largestGrid(grid.getSumGrid(3),3))
	print(largestSquare(grid))
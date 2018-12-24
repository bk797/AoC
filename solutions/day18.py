from enum import Enum
from functools import reduce
file = '../inputs/day18.txt'
sample = '../inputs/sample.txt'
class Type(Enum):
	openGround = '.'
	trees = '|'
	lumberyard = '#'

class Outskirt:

	def __init__(self,grid):
		self.grid = grid

	def transform(self):
		newGrid = []
		for row in range(0,len(self.grid)):
			newRow = []
			for col in range(0,len(self.grid[row])):
				newRow.append(self.nextState(row,col))
				# print("after",row,col,newRow[-1])
			newGrid.append(newRow)
		self.grid = newGrid

	def nextState(self,row,col):
		type = self.grid[row][col]
		# print(row,col,type)
		adj = self.getAdjacent(row,col)
		if type == Type.openGround:
			return Type.openGround if len(list(filter(lambda x: x == Type.trees,adj))) < 3 else Type.trees
		elif type == Type.trees:
			return Type.trees if len(list(filter(lambda x: x == Type.lumberyard,adj))) < 3 else Type.lumberyard
		elif type == Type.lumberyard:
			return Type.lumberyard if Type.lumberyard in adj and Type.trees in adj else Type.openGround
		else:
			raise Exception

	def getAdjacent(self,row,col):
		adj = []
		for r in range(row-1,row+2):
			for c in range(col-1,col+2):
				try:
					if not (r < 0 or c < 0):
						if not (r == row and c == col):
							adj.append(self.grid[r][c])
				except:
					continue
		return adj

	def getValue(self):
		yards = 0
		trees = 0
		for row in self.grid:
			for char in row:
				if char == Type.lumberyard:
					yards += 1
				elif char == Type.trees:
					trees += 1
		return yards * trees

	def valueAfterMins(self,minutes):
		gridStrings = {}
		grids = []
		grids.append(self.grid)
		gridStrings[self.__str__()] = 0
		for i in range(1,minutes):
			self.transform()
			gridStr = self.__str__()
			if gridStr not in gridStrings:
				grids.append(self.grid)
				gridStrings[gridStr] = i
			else:
				first = gridStrings[gridStr]
				index = (minutes-first) % (i-first) + first
				print(minutes,first,len(gridStrings))
				self.grid = grids[index]
				break
		return self.getValue()

	def __str__(self):
		string = ''
		for row in self.grid:
			string += reduce(lambda x,y: x + y.value,row,'') + '\n'
		return string

def buildOutskirt(lines):
	grid = []
	for line in lines:
		line = line.strip()
		row = []
		for char in line:
			row.append(Type(char))
		grid.append(row)
	return Outskirt(grid)

if __name__ == '__main__':
	lines = open(file,'r').readlines()
	# lines = open(sample,'r').readlines()
	outskirts = buildOutskirt(lines)
	print(outskirts.getValue())
	print(outskirts.valueAfterMins(1000000000))
	print(outskirts)
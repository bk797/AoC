import networkx as nx
file = '../inputs/day22.txt'
symbols = ".=|"

class Cave:

	def __init__(self,depth,target):
		self.depth = depth
		self.target = target
		self.grid = []
		self.formGeologicIndices()
		self.formErosionLevel()

	def formGeologicIndices(self):
		x,y = self.target
		dim = x if x > y else y
		dim = int(dim*1.5)
		multiplier = 30
		yRange = (y*multiplier) if (y*multiplier) < dim else dim
		xRange = (x*multiplier) if (x*multiplier) < dim else dim
		print(xRange,yRange)
		self.grid.append([(i * 16807+self.depth)% 20183 for i in range(0,int(xRange)+1)])
		for r in range(1,int(yRange)+1):
			row = [(r*48271+self.depth)% 20183]
			for c in range(1,int(xRange)+1):
				row.append((self.grid[r-1][c] * row[c-1] + self.depth)%20183)
			self.grid.append(row)

	def buildGraph(self):
		self.graph = nx.Graph()
		for row in range(0,len(self.grid)):
			for col in range(0,len(self.grid[row])):
				tools = toolsForTerrain(self.grid[row][col])
				for t in tools:
					self.graph.add_node((row,col,t))
					for a in getAdjacent(row,col):
						aR,aC = a
						if self.validCoor(*a) and canPass(self.grid[aR][aC],t):
							self.graph.add_edge((row,col,t),(aR,aC,t),weight=1)
						# else:
						# if self.validCoor
				self.graph.add_edge((row,col,tools[0]),(row,col,tools[1]),weight=7)
		x,y = self.target
		length = nx.algorithms.shortest_path_length(self.graph,(0,0,"torch"),(y,x,"torch"),"weight")
		print(length)

	def formErosionLevel(self):
		for row in self.grid:
			for c in range(0,len(row)):
				row[c] = row[c] % 3
		x,y = self.target
		self.grid[0][0] = 0
		self.grid[y][x] = 0 #set target location rocky

	def __str__(self):
		gridStr = ''
		for row in self.grid:
			for col in row:
				gridStr += symbols[col]
			gridStr += '\n'
		return gridStr

	def calculateRisk(self):
		risk = 0
		for r in range(0,self.target[1]+1):
			for c in range(0,self.target[0]+1):
				risk += self.grid[r][c]
		return risk

	def validCoor(self,y,x):
		if y < 0 or x < 0:
			return False
		if y >= len(self.grid) or x >= len(self.grid[y]):
			return False
		return True

def toolsForTerrain(terrain):
	tools = ["neither","torch","cg"]
	if terrain == 0:
		tools.remove("neither")
	elif terrain == 1:
		tools.remove("torch")
	elif terrain == 2:
		tools.remove("cg")
	return tools

def canPass(terrain,tool):
	if terrain == 0:
		return tool != "neither"
	elif terrain == 1:
		return tool != "torch"
	else:
		return tool != "cg"

def getAdjacent(y,x):
	return[(y-1,x),(y,x-1),(y,x+1),(y+1,x)]

if __name__ == '__main__':
	depth = 5616
	target = (10,785)
	# depth = 510
	# target = (10,10)
	cave = Cave(depth,target)
	# print(cave)
	print(cave.calculateRisk())
	# print(cave.shortestDistance())
	cave.buildGraph()

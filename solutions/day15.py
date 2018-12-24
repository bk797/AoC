from functools import reduce
file = '../inputs/day15.txt'
HIT_POINTS = 200
DAMAGE = 3
SPECIES = 'GE'

class Unit:

	def __init__(self,species,pos,dmg):
		self.species = species
		self.hp = HIT_POINTS
		self.dmg = dmg
		self.pos = pos
		self.alive = True

	def hit(self,damage):
		self.hp -= damage
		if self.hp < 1:
			self.alive = False

class Square:

	def __init__(self,type):
		self.type = type
		self.occupied = None

	def remove(self):
		self.occupied = None

	def occupy(self,piece):
		self.occupied = piece

class Field:

	def __init__(self,board,pieces):
		self.board = board
		self.pieces = pieces

	def getOutcome(self):
		turns = self.fight()
		remainingHp = reduce(lambda x,y: x + y.hp,self.pieces,0)
		return remainingHp * turns

	def elvesLost(self):
		elves = len(list(filter(lambda x: x.species == 'E',self.pieces)))
		self.fight()
		return elves - len(list(filter(lambda x: x.species == 'E',self.pieces)))

	def fight(self):
		turns = 0		
		while True:
			self.pieces.sort(key=lambda x:x.pos,reverse=False) #put pieces in reading order
			end = self.round()
			self.pieces = list(filter(lambda x: x.alive,self.pieces))
			if end is 0:
				break #move each piece
			turns += 1
			remainingElves = len(list(filter(lambda x: x.species == 'E',self.pieces)))
			if remainingElves is 0 or remainingElves is len(self.pieces):
				break
		return turns

	def round(self):
		for piece in self.pieces:
			if not piece.alive:
				continue
			#only one faction left
			elif len(list(filter(lambda x: x.species != piece.species and x.alive, self.pieces))) == 0:
				return 0
			else:
				self.turn(piece)
		return 1

	def turn(self,piece):
		x,y = piece.pos
		enemy = self.closestEnemy(piece)
		if enemy is not None:
			#move phase
			dist = self.distance(piece.pos,enemy.pos)
			if dist > 1:
				for adjPos in getAdjacent(x,y):
					newX,newY = adjPos
					if self.board[newX][newY].occupied:
						continue
					if self.distance(adjPos,enemy.pos)+1 == dist:
						self.board[x][y].remove()
						self.board[newX][newY].occupy(piece)
						piece.pos = adjPos
						break
			#attack phase
			enemy = self.adjacentEnemy(piece)
			if enemy is not None:
				enemy.hit(piece.dmg)
				if not enemy.alive:
					eX,eY = enemy.pos
					self.board[eX][eY].remove()


	#if enemy exists, find enemy that has the lowest hp, ties broken by reading order
	def adjacentEnemy(self,piece):
		enemy = None
		for adjPos in getAdjacent(*piece.pos):
			x,y = adjPos
			adjPiece = self.board[x][y].occupied
			if adjPiece is not None and adjPiece.species is not piece.species:
				if enemy is None:
					enemy = adjPiece
				elif adjPiece.hp < enemy.hp:
					enemy = adjPiece
		return enemy


	#find the closest spot next to an enemy to move towards. ties are broken by reading order
	def closestEnemy(self,piece):
		queue = [(piece.pos,0)]
		visited = []
		enemies = []
		minDist = -1
		while len(queue) > 0:
			node,dist = queue.pop(0)
			if minDist is not -1 and dist > minDist:
				break
			for adjPos in getAdjacent(*node):
				x,y = adjPos
				adjSquare = self.board[x][y]
				inQueue = reduce(lambda x,y: x or y[0] == adjPos,queue,False)
				if inQueue or adjPos in visited:
					continue
				adjPiece = adjSquare.occupied
				if adjPiece is not None:
					if adjPiece.alive and piece.species is not adjPiece.species:
						enemies.append([adjPiece,node])
						minDist = dist
				elif adjSquare.type is '.':
					queue.append((adjPos,dist+1))
			visited.append(node)
		if len(enemies) is 0:
			return None
		else:
			enemies.sort(key=lambda x: x[1],reverse=False)
			return enemies[0][0]

	#calcalute shortest distance between two points
	def distance(self,posA,posB):
		square = self.board[posA[0]][posA[1]]
		if square.type is '#': 
			return -1
		queue = [(posA,0)]
		visited = []
		while len(queue) > 0:
			node,dist = queue.pop(0)
			for adjPos in getAdjacent(*node):
				if adjPos == posB:
					return dist+1
				x,y = adjPos
				adjSquare = self.board[x][y]
				inQueue = reduce(lambda x,y: x or y[0] == adjPos,queue,False)
				if inQueue or adjPos in visited:
					continue
				adjPiece = adjSquare.occupied
				if adjPiece is not None or adjSquare.type is '#':
					continue
				queue.append((adjPos,dist+1))
			visited.append(node)
		return -1


def getAdjacent(row,col):
	return[(row-1,col),(row,col-1),(row,col+1),(row+1,col)]


'''
	builds the BattleField by adding the Squared and Units
'''
def buildField(lines,G,E):
	grid = []
	pieces = []
	r = 0
	for line in lines:
		line = line.strip()
		row = []
		c = 0
		for char in line:
			if char is '.':
				row.append(Square('.'))
			elif char in SPECIES:
				square = Square('.')
				if char is 'G':
					unit = Unit(char,(r,c),G)
				elif char is 'E':
					unit = Unit(char,(r,c),E)
				square.occupy(unit)
				row.append(square)
				pieces.append(unit)
			else:
				row.append(Square('#'))
			c += 1
		grid.append(row)
		r+=1
	return Field(grid,pieces)

'''
	print grid for debugging
'''
def printGrid(grid):
	strGrid = ''
	for row in grid:
		strGrid += reduce(lambda x,y: x + (y.occupied.species if y.occupied is not None else y.type),row,'') + '\n'
	print(strGrid)

if __name__ == "__main__":
	lines = open(file,'r').readlines()
	field = buildField(lines,3,3)
	#get the outcome with default numbers
	printGrid(field.board)
	print(field.getOutcome())
	printGrid(field.board)
	PE = 3
	E = 6
	#find bounds
	while True:
		field = buildField(lines,3,E)
		if field.elvesLost() == 0:
			#binary search
			while E-PE > 1:
				mid = PE+(E-PE)//2
				field = buildField(lines,3,mid)
				lost = field.elvesLost()
				print(PE,E,mid,lost)
				if lost > 0:
					PE = mid
				else:
					E = mid
			break
		PE = E
		E *= 2
	#find oucome with new elves p ower
	field = buildField(lines,3,E)
	print(field.getOutcome())
file = '../inputs/day23.txt'
import math

class NanoBot:

	def __init__(self,pos,range):
		self.pos = pos
		self.range =  range

	def __str__(self):
		return '%d,%d,%d'%(self.pos[0],self.pos[1],self.pos[2])

def manhattanDistance(p1,p2):
	x1,y1,z1 = p1
	x2,y2,z2 = p2
	return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

def getNanoBot(line):
	pos,botRange = line.split(' ')
	pos=pos.split('=')[-1]
	pos = pos.replace('<','').replace('>,','').split(',')
	pos = list(map(lambda x:int(x),pos))
	botRange = int(botRange.split('=')[-1])
	return NanoBot(pos,botRange)

def getNanoBots(lines):
	bots = []
	for line in lines:
		bots.append(getNanoBot(line))
	bots.sort(key=lambda x: x.range,reverse=True)
	return bots

def countInRange(bots):
	strongest = bots[0]
	count = 1
	for i in range(1,len(bots)):
		bot = bots[i]
		if manhattanDistance(strongest.pos,bot.pos) <= strongest.range:
			count += 1
	return count

def allInRange(bounds,pos,mRange):
	minX,maxX,minY,maxY,minZ,maxZ = bounds
	positions = []
	lowerX = pos[0] - mRange
	upperX = pos[0] + mRange+1
	lowerX = minX if minX > lowerX else lowerX
	upperX = maxX if maxX < upperX else upperX
	for x in range(lowerX,upperX):
		yRange = mRange-(pos[0]-x)
		lowerY = pos[1] - yRange
		upperY = pos[1] + yRange+1
		lowerY = minY if minY > lowerY else lowerY
		upperY = maxY if maxY < upperY else upperY
		for y in range(lowerY,upperY):
			zRange = mRange-(pos[0]-x)-(pos[1]-y)
			lowerZ = pos[2]-zRange
			upperZ = pos[2]+zRange+1
			lowerZ = minZ if minZ > lowerZ else lowerZ
			upperZ = maxZ if maxZ < upperZ else upperZ
			for z in range(lowerZ,upperZ):
				positions.append((x,y,z))
	return positions

def findRanges(bots):
	minX,minY,minZ = [10000000000000000000000000 for i in range(0,3)]
	maxX,maxY,maxZ = [-100000000000000000000000000 for i in range(0,3)]
	for bot in bots:
		x,y,z = bot.pos
		minX = x if x < minX else minX
		minY = y if y < minY else minY
		minZ = z if z < minZ else minZ
		maxX = x if x > maxX else maxX
		maxY = y if y > maxY else maxY
		maxZ = z if z > maxZ else maxZ
	return [minX,maxX+1,minY,maxY+1,minZ,maxZ+1]

def mostRanges(bots):
	bounds = findRanges(bots)
	for i in range(0,len(bounds)):
		if bounds[i] > 0:
			bounds[i] = int(math.sqrt(bounds[i]))
		else:
			bounds[i] = int(-math.sqrt(-bounds[i]))
	# minX,maxX,minY,maxY,minZ,maxZ = findRanges(bots)
	minX,maxX,minY,maxY,minZ,maxZ = bounds
	# print(minX,maxX,minY,maxY,minZ,maxZ)
	ranges = {}
	for x in range(minX,maxX):
		for y in range(minY,maxY):
			for z in range(minZ,maxZ):
				pos = (x,y,z)
				ranges[pos] = 0
				for bot in bots:
					if manhattanDistance(pos,bot.pos) <= bot.range:
						ranges[pos] += 1
	most = max(ranges,key=ranges.get)
	mostList = [p for p in ranges if ranges[p] == ranges[most]]
	minPos = min(mostList,key=lambda x: manhattanDistance((0,0,0),x))
	return minPos

def inRangeOfMost(bots):
	bounds = findRanges(bots)
	print(bounds)
	ranges = {}
	for i in range(0,len(bots)):
		bot = bots[i]
		for r in allInRange(bounds,bot.pos,bot.range):
			x,y,z = bot.pos
			pos = r
			if pos not in ranges:
				ranges[pos] = 1
			else:
				ranges[pos] += 1			
	most = max(ranges,key=ranges.get)
	mostList = list(filter(lambda x: ranges[x] == ranges[most],ranges.keys()))
	print(mostList)
	return min(mostList,key=lambda x: manhattanDistance((0,0,0),x))


if __name__ == '__main__':
	lines = open(file,'r').readlines()
	bots = getNanoBots(lines)
	print(countInRange(bots))
	print(manhattanDistance(inRangeOfMost(bots),(0,0,0)))

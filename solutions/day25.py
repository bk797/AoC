import networkx as nx
file = '../inputs/day25.txt'

def manhattanDistance(p1,p2):
	dist = 0
	for i in range(len(p1)):
		dist += abs(p1[i]-p2[i])
	return dist

def getPoint(line):
	return tuple(map(lambda x: int(x),line.split(',')))

def getPoints(lines):
	uf = nx.utils.UnionFind()
	for line in lines:
		uf[getPoint(line)]
	return uf

def countGroups(uf):
	noMatches = list(uf)
	# matches = []
	for i in range(0,len(noMatches)):
		point = noMatches[i]
		for j in range(1,len(noMatches)):
			otherPoint = noMatches[j]
			if uf[point] != uf[otherPoint]:
				if manhattanDistance(point,otherPoint) <= 3:
					uf.union(point,otherPoint)
	values = set()
	for u in uf:
		values.add(uf[u])
	return len(values)

if __name__ == '__main__':
	lines = open(file,'r').readlines()
	uf = getPoints(lines)
	print(countGroups(uf))


from functools import reduce

sample = '../inputs/sample.txt'
file = '../inputs/day7.txt'

class Node:

	def __init__(self,id):
		self.id = id
		self.children = []
		self.parents = 0

	def addChild(self,childId):
		self.children.append(childId)

	def addParent(self):
		self.parents += 1

	def removeParent(self):
		self.parents -= 1

	def hasParents(self):
		return self.parents > 0

class DAG:

	def __init__(self):
		self.nodes = {}
		self.noParents = []

	def add(self,node):
		self.nodes[node.id] = node

	def addRelation(self,pId,cId):
		if pId not in self.nodes:
			self.nodes[pId] = Node(pId)
		if cId not in self.nodes:
			self.nodes[cId] = Node(cId)
		self.nodes[pId].addChild(cId)
		self.nodes[cId].addParent()

	def checkOrphans(self):
		self.noParents = []
		for id in self.nodes.keys():
			if not self.nodes[id].hasParents():
				self.noParents.append(id)
		self.noParents.sort()

	def remove(self,id):
		for c in self.nodes[id].children:
			# print('next key %s' % c)
			self.nodes[c].removeParent()
			if not self.nodes[c].hasParents():
				self.noParents.append(c)
		self.noParents.sort()
		del self.nodes[id]		

	def pop(self):
		self.checkOrphans()
		id = self.noParents.pop(0)
		self.remove(id)
		return id

	def getAvailable(self):
		self.checkOrphans()
		return self.noParents

	def notEmpty(self):
		return len(self.nodes.keys()) != 0


def buildDag(lines):
	dag = DAG()
	for line in lines:
		words = line.split(' ')
		parent = words[1]
		child = words[-3]
		dag.addRelation(parent,child)
	return dag

def getOrder(dag):
	order = []
	while dag.notEmpty():
		order.append(dag.pop())
	return order

def totalTime(dag,workers,baseSteps):
	time = 0
	working = set()
	stepsLeft = []
	for i in range(0,workers):
		stepsLeft.append((-1,''))
	while dag.notEmpty():
		for i in range(0,workers):
			s = stepsLeft[i]
			if s[0] == 0:
				dag.remove(s[1])
				stepsLeft[i] = (-1,'')
		available = dag.getAvailable()
		available = list(filter(lambda x: x not in working,available))
		for i in range(0,workers):
			s = stepsLeft[i]
			if s[0] < 0 and len(available) > 0:
				letter = available.pop(0)
				stepsLeft[i] = (getTime(baseSteps,letter),letter)
				working.add(letter)
		stepping = list(filter(lambda x: x[0] > 0,stepsLeft))
		timeShift = reduce(lambda x,y:x if x < y[0] else y[0],stepping,120)
		if timeShift != 120:
			stepsLeft = list(map(lambda x: (x[0]-timeShift,x[1]),stepsLeft))
			time += timeShift
	return time

def getTime(baseSteps,letter):
	baseLetter = ord('A')-1
	return baseSteps + ord(letter)-baseLetter


if __name__ == '__main__':
	lines = open(file,'r').readlines()
	dag = buildDag(lines)
	print(''.join(getOrder(dag)))
	dag = buildDag(lines)
	print(totalTime(dag,5,60))

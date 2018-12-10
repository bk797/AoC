from functools import reduce
file = '../inputs/day8.txt'

class Node:

	def __init__(self):
		self.val = -1
		self.children = []
	
	def setValue(self,metadata):
		n = len(self.children)
		if n == 0:
			self.val = reduce(lambda acc,e: acc + e,metadata,0)
			return
		sum = 0
		for i in metadata:
			if i <= n:
				sum += self.children[i-1].val
		self.val = sum

	def addChild(self,child):
		self.children.append(child)

class Tree:

	def __init__(self,line):
		self.stream = line.split(' ')

	def buildTree(self):
		children = self.pop()
		metaCount = self.pop()
		metadata = []
		head = Node()
		for i in range(0,children):
			head.addChild(self.buildTree())
		for i in range(0,metaCount):
			metadata.append(self.pop())
		head.setValue(metadata)
		return head

	def pop(self):
		return int(self.stream.pop(0))


class Stream:

	def __init__(self,line):
		self.stream = line.split(' ')

	def getSum(self):
		children = self.pop()
		meta = self.pop()
		sum = 0
		for i in range(0,children):
			sum += self.getSum()
		for i in range(0,meta):
			sum += self.pop()
		return sum

	def pop(self):
		return int(self.stream.pop(0))




if __name__ == '__main__':
	line = open(file,'r').readline()
	stream = Stream(line)
	print(stream.getSum())
	tree = Tree(line)
	print(tree.buildTree().val)
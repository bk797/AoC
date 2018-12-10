file = '../inputs/day5.txt'
sample = '../inputs/sample.txt';

def react(polymer):
	stack = []
	for p in polymer:
		if len(stack) == 0:
			stack.append(p)
		elif shouldDestroy(stack[-1],p):
			stack.pop()
		else:
			stack.append(p)
	return len(stack)

def shouldDestroy(i1,i2):
	return abs(ord(i1)-ord(i2)) == 32

def shortest(polymer):
	distinct = list(set(polymer.lower()))
	min = len(polymer)
	for c in distinct:
		filterBy = filterString(c)
		filteredPolymer = list(filter(lambda x: x not in filterBy,polymer))
		l = react(filteredPolymer)
		if l < min:
			min = l
	return min

def filterString(c):
	captialChar = ord(c) - 32
	return c+chr(captialChar)

if __name__ == '__main__':
	# polymer = open(sample,'r').readline()
	polymer = open(file,'r').readline()
	print(react(polymer))
	print(shortest(polymer))
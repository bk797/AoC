file = '../inputs/day12.txt'
sample = '../inputs/sample.txt'

class Garden:

	def __init__(self,state,spread):
		self.state = state
		self.spread = spread
		self.initialPos = 0

	def nextGeneration(self):
		newState = ['.','.']
		self.expand(4)
		for i in range(2,len(self.state)-3):
			plants = self.getPlants(i)
			if plants in self.spread:
				newState.append('#')
			else:
				newState.append('.')
		self.state = newState
		self.trim()

	def expand(self,size):
		for i in range(0,size):
			self.state.append('.')
			self.state.insert(0,'.')
		self.initialPos -= size
 
	def getPlants(self,i):
		return ''.join(self.state[i-2:i+3])

	def trim(self):
		while self.state[0] is '.':
			self.state.pop(0)
			self.initialPos += 1
		while self.state[-1] is '.':
			self.state.pop()

	def sum(self):
		sum = 0
		for i in range(0, len(self.state)):
			if self.state[i] is '#':
				sum += self.initialPos + i
		return sum

	def stateString(self):
		return ''.join(self.state)


def toInitialState(line):
	return list(line.split(' ')[-1])

def toPlant(line):
	condition,result = line.split(' => ')
	if result is '#':
		return condition
	else:
		return None

'''
	The rate in which the sum of the pots change converges to a number, so as long as we find that number
	you can extrapolate the sum after a very large number of generations

'''
def getSumAfter(garden,generation):
	same = 0
	prevSum = garden.sum()
	prevDif = 0
	for i in range(0,generation):
		garden.nextGeneration()
		curSum = garden.sum()
		curDif = curSum-prevSum
		if curDif is prevDif:
			same += 1
		else:
			same = 0
		prevSum = curSum
		prevDif = curDif
		if same is 100:
			return prevSum + (generation-(i+1))*prevDif
	return prevSum


if __name__ == '__main__':
	pots = open(file,'r').read().splitlines();
	# pots = open(sample,'r').read().splitlines();
	state = toInitialState(pots[0])
	spread = list(map(lambda x: toPlant(x),pots[2:]))
	spread = list(filter(lambda x: x is not None,spread))
	garden = Garden(state,spread)
	print(getSumAfter(garden,20))
	print(getSumAfter(garden,50000000000-20)) #already did 20 generations

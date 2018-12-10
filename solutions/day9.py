from collections import deque
from functools import reduce
file = '../inputs/day9.txt'

def getParams(line):
	words = line.split(' ')
	return [int(words[0]),int(words[-2])] #inclusive upper bound

def initializeList(size,initialValue):
	arr = []
	for i in range(0,size):
		arr.append(initialValue)
	return arr

def getMax(list):
	return reduce(lambda x,y: y if y > x else x,list)

def playGame(players,maxMarble):
	scores = initializeList(players,0)
	circle = deque([0])
	index = 1
	turn = 1
	for nextMarble in range(1,maxMarble+1):
		if nextMarble % 23 == 0:
			circle.rotate(8)
			scores[turn] += circle.popleft() + nextMarble
			circle.rotate(-1)
		else:
			circle.rotate(-1)
			circle.appendleft(nextMarble)
			circle.rotate(-1)
		turn = (turn+1) % players
	return getMax(scores)

if __name__ == '__main__':
	line = open(file,'r').readline()
	params = getParams(line)
	print(playGame(*params))
	print(playGame(params[0],params[1]*100))
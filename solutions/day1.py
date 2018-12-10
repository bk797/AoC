from functools import reduce
file = '../inputs/day1.txt'

#sum reducer 
def findFrequency(ops):
	return reduce(lambda acc,x: acc + x,ops,0)

#looks for the first time a frequency is seen twice
#the frequency is the sum of all of the previous operations
def findFirstRepeat(ops):
	frequencies = set()
	f = 0
	while True:
		for op in ops:
			f += op
			if f in frequencies:
				return f
			else:
				frequencies.add(f)

if __name__ == '__main__':
	#read input and convert it each entry to an int
	puzzleInput = open(file,'r')
	ops = puzzleInput.readlines()
	ops = list(map(int,ops))
	#run the two problems
	print(findFrequency(ops))
	print(findFirstRepeat(ops))
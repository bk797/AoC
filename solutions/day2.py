file = '../inputs/day2.txt';


def countLetters(id):
	letters = {}
	for c in id:
		if c in letters:
			letters[c] += 1
		else:
			letters[c] = 1
	return letters.values()

def hasCount(lCount,num):
	return num in lCount

def part1(boxIds):
	letterCounts = list(map(lambda id:countLetters(id),boxIds))
	twoLetters = list(filter(lambda count: hasCount(count,2),letterCounts))
	threeLetters = list(filter(lambda count:hasCount(count,3),letterCounts))
	return len(twoLetters) * len(threeLetters)

def isOneAway(id1,id2):
	#assume same length and not empty
	n = len(id1)
	hasDif = False
	for i in range(0,n):
		if id1[i] != id2[i]:
			if hasDif:
				return False
			else:
				hasDif = True
	return hasDif

def compare(id1):
	def compareWith(id2):
		return isOneAway(id1,id2)
	return compareWith

def part2(boxIds):
	for i in range(0,len(boxIds)-1):
		box1 = compare(boxIds[i])
		match = list(filter(lambda id:box1(id),boxIds[i+1:]))
		if len(match):
			return getMatching(boxIds[i],match[0])

def getMatching(id1,id2):
	n = len(id1)
	id = ""
	for i in range(0,n):
		if id1[i] == id2[i]:
			id += id1[i]
	return id.strip()

if __name__ == '__main__':
	boxIds = open(file,'r').readlines()
	print(part1(boxIds))
	print(part2(boxIds))
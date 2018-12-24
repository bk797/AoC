from functools import reduce
input = '077201'
start = '37'

def produceRecipes(recipes,iA,iB):
	return str((int(recipes[iA]) + int(recipes[iB])))

def getNewIndices(recipes,iA,iB):
	rLen = len(recipes)
	newA = (iA + 1 + int(recipes[iA])) % rLen
	newB = (iB + 1 + int(recipes[iB])) % rLen
	return (newA,newB)

def findNextTen(recipes,input):
	iA,iB = [0,1]
	while len(recipes) < input+10:
		recipes += produceRecipes(recipes,iA,iB)
		iA,iB = getNewIndices(recipes,iA,iB)
	return recipes[input:]

def findPadding(recipes,input):
	iA,iB = [0,1]
	n = len(input)
	#need to search n-1 space in the case where you get your number when the elves score is at least 10
	while input not in recipes[-n-1:] :
		if len(recipes) % 20000000 == 0:
			print('20 million!')
		recipes += produceRecipes(recipes,iA,iB)
		iA,iB = getNewIndices(recipes,iA,iB)
	return len(recipes)-n-1


if __name__ == '__main__':
	recipes = start
	print(findNextTen(recipes,int(input)))
	recipes = start
	print(findPadding(recipes,input))

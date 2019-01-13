file = '../inputs/day20.txt'

plotMap = {(0,0):0}

def strToVector(dir):
	if dir == 'N':
		return (0,-1)
	elif dir == 'S':
		return (0,1)
	elif dir == 'E':
		return (1,0)
	else:
		return (-1,0)

def getLargest():
	global plotMap
	largest = 0
	for p in plotMap.keys():
		largest = plotMap[p] if plotMap[p] > largest else largest
	return largest

'''
	The idea is that I store every position that the path goes through in a Dict, and
	the Dict (plotMap) will store the shortest path to any give position on the map
'''
def explore(line,pos,index=1,pathLen=0):
	global plotMap
	curPos = pos
	curLen = pathLen
	while line[index] not in ')|$':
		char = line[index]
		if char in 'NSEW':
			dir = strToVector(char)
			curPos = (curPos[0]+dir[0],curPos[1]+dir[1])
			curLen += 1
			if curPos not in plotMap:
				plotMap[curPos] = curLen
			else:
				if curLen < plotMap[curPos]:
					plotMap[curPos] = curLen
		elif char == '(':
			index,exploreLen = explore(line,curPos,index+1,curLen)
			curLen = exploreLen
		index += 1
	if line[index] == '|':
			index,otherLen = explore(line,pos,index+1,pathLen)
			curLen = otherLen if otherLen < curLen else curLen
	return (index,curLen)

def countPathsWithDistance(dis):
	global plotMap
	count = 0
	for p in plotMap.keys():
		count += 0 if plotMap[p] < dis else 1
	return count

if __name__ == '__main__':
	line = open(file,'r').read()
	# print(longestPath(line))
	explore(line,(0,0))
	# print(plotMap)
	print(getLargest())
	print(countPathsWithDistance(1000))

file = "../inputs/day4.txt"

def getMinute(log):
	return int(log.split(']')[0].split(' ')[-1].split(':')[-1])

def hourLog():
	arr = []
	for i in range(0,60):
		arr.append(0)
	return arr

def getId(map):
	guardId = getGuard(map)
	minute = maxMinute(map[guardId])
	return int(guardId) * int(minute)

def getGuard(map):
	guardId = None
	max = 0
	for k in map.keys():
		count = sum(map[k])
		if count > max:
			max = count
			guardId = k
	return guardId

def maxMinute(arr):
	index = -1
	max = 0
	for i in range(0,len(arr)):
		if arr[i] > max:
			max = arr[i]
			index = i
	return index

def buildMap(logs):
	map = {}
	guardId = None
	sleepStart = None
	for log in logs:
		if "begins shift" in log:
			guardId = log.split("#")[-1].split(' ')[0]
			if guardId not in map:
				map[guardId] = hourLog()
		elif "falls asleep" in log:
			sleepStart = getMinute(log)
		else:
			sleepEnd = getMinute(log)
			for i in range(sleepStart, sleepEnd):
				map[guardId][i] += 1
	return map

def getNapper(map):
	guardId = None
	index = None
	max = 0
	for k in map.keys():
		for i in range(0,len(map[k])):
			c = map[k][i]
			if c > max:
				index = i
				guardId = k
				max = c
	return int(guardId) * index

if __name__ == '__main__':
	logs = open(file,'r').readlines()
	logs.sort()
	map = buildMap(logs)
	print(getId(map))
	print(getNapper(map))
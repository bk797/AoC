file = '../inputs/day3.txt';

def overlap(entries):
	cloth = {}
	ids = set()
	for entry in entries:
		plot(entry,cloth,ids)
	count = 0
	ones = 0
	for r in cloth.keys():
		for c in cloth[r].keys():
			if len(cloth[r][c]) > 1:
				count += 1
				for id in cloth[r][c]:
					ids.discard(id)
	print(ids.pop()) #part 2
	return count # part 1

def plot(entry,cloth,ids):
	claimId,rect = entry.split('@')
	ids.add(claimId)
	coor = rect.split(':')
	x,y = coor[0].strip().split(',');
	xD,yD = coor[1].strip().split('x');
	x = int(x)
	y = int(y)
	xD = int(xD)
	yD = int(yD)
	for r in range(y,y+yD):
		for c in range(x,x+xD):
			if r not in cloth:
				cloth[r] = {c:[claimId]}
			elif c not in cloth[r]:
				cloth[r][c] = [claimId]
			else:
				cloth[r][c].append(claimId)

if __name__ == '__main__':
	entries = open(file,'r').readlines()
	print(overlap(entries))
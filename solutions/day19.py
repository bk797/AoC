file = '../inputs/day19.txt'

# runs op with given operation function
def op(func,type,a,b,c,reg):
	n = len(reg)
	reg = reg.copy()
	if type == 'r' or type == 'rr':	
		if a < n and b < n:
			return func(reg[a],reg[b],c,reg)
	if type == 'i' or type == 'ri':
		if a < n:
			if func is ass:
				return func(a,b,c,reg)
			else:
				return func(reg[a],b,c,reg)
	if type == 'ir':
		if b < n:
			return func(a,reg[b],c,reg)
	else:
		raise Exception

'''
  functions of operations
'''
def ban(a,b,c,reg):
	reg[c] = a & b
	return reg

def mul(a,b,c,reg):
	reg[c] = a * b
	return reg

def bor(a,b,c,reg):
	reg[c] = a | b
	return reg

def add(a,b,c,reg):
	reg[c] = a + b
	return reg

def ass(a,b,c,reg):
	reg[c] = a
	return reg

def gt(a,b,c,reg):
	reg[c] = 1 if a > b else 0
	return reg

def eq(a,b,c,reg):
	reg[c] = 1 if a == b else 0
	return reg

def operate(opCode,a,b,c,reg):
	if 'add' in opCode:
		return op(add,opCode[-1],a,b,c,reg)
	elif 'mul' in opCode:
		return op(mul,opCode[-1],a,b,c,reg)
	elif 'ban' in opCode:
		return op(ban,opCode[-1],a,b,c,reg)
	elif 'bor' in opCode:
		return op(bor,opCode[-1],a,b,c,reg)
	elif 'set' in opCode:
		return op(ass,opCode[-1],a,b,c,reg)
	elif 'gt' in opCode:
		return op(gt,opCode[-2:],a,b,c,reg)
	elif 'eq' in opCode:
		return op(eq,opCode[-2:],a,b,c,reg)

def instructionOps(ip,ops,register):
	count = 1
	while register[ip] < len(ops):
		print(register)
		if count % 40 == 0:
			break
		index = register[ip]
		register = operate(*ops[index],register)
		register[ip] += 1
		count += 1
	# return register

def readLines(lines):
	ip = int(lines[0].split(' ')[-1])
	ops = []
	for line in lines[1:]:
		opCode,a,b,c = line.split(' ')
		ops.append([opCode,int(a),int(b),int(c)])
	return (ip,ops)

if __name__ == '__main__':
	lines = open(file,'r').readlines()
	inputs = readLines(lines)
	part1Register = [0,0,0,0,0,0]
	# print(instructionOps(*inputs,part1Register))
	part2Register = [1,0,0,0,0,0]
	print(instructionOps(*inputs,part2Register))

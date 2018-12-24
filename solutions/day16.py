part1 = '../inputs/day16p1.txt'
part2 = '../inputs/day16p2.txt'
sample = '../inputs/sample.txt'

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

opCodes = ['addr','addi','mulr','muli','banr','bani','borr','bori','setr','seti','gtir','gtri','gtrr','eqir','eqri','eqrr']

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

#see if opcode + rI provides rA
def doesMatch(opCode,a,b,c,rI,rA):
	try:
		result = operate(opCode,a,b,c,rI)
		if result == rA:
			# print(opCode,a,b,c)
			return True
		else:
			return False
	except:
		return False

#get all the possible matches for a instruction given a before and after
def countMatching(a,b,c,rI,rA):
	possible = []
	for code in opCodes:
		if doesMatch(code,a,b,c,rI,rA):
			possible.append(code)
	return possible

#find the number of ins that have at least limi amount of possible codes
def sumBehaviors(ins,limit):
	sum = 0
	for i in ins:
		op,rI,rA = i
		if len(countMatching(*op[1:],rI,rA)) >= limit:
			sum +=1
	return sum

#convert lines into an op, before, and after register
def readInstruction(lineA,lineB,lineC):
	rI = eval(lineA.split(': ')[1])
	rA = eval(lineC.split(': ')[1])
	op = list(map(lambda x: int(x),lineB.strip().split(' ')))
	return (op,rI,rA)

#read sample input
def readInput(lines):
	instructions = []
	for i in range(0,len(lines),4):
		instruction = lines[i:i+3]
		ins = readInstruction(*instruction)
		instructions.append(ins)
	return instructions

#given the sampel input determines which opCode corresponds to which command
def determineOpCodes(ins):
	codes = {}
	#fill up initial possiblities
	for i in ins:
		op,rI,rA = i
		opCode = op[0]
		matches = countMatching(*op[1:],rI,rA)
		if opCode not in codes:
			codes[opCode] = matches
		else:
			codes[opCode] = list(filter(lambda x: x in matches,codes[opCode]))
	#if a opCode has only one mapping, then remove said mapping from the other opCode possiblities
	while not determinedCodes(codes):
		for code in codes.keys():
			matches = codes[code]
			if len(matches) == 1:
				for otherCode in codes.keys():
					if otherCode != code:
						if matches[0] in codes[otherCode]:
							codes[otherCode].remove(matches[0])
	for k in codes.keys():
		codes[k] = codes[k][0]
	return codes

#check to see if each code has a single mapping
def determinedCodes(codes):
	for k in codes.keys():
		possible = codes[k]
		if len(possible) != 1:
			return False
	return True

# run each of the operations on the register (starts at [0,0,0,0])
def runOps(ops,codeMap):
	register = [0,0,0,0]
	for op in ops:
		op = list(map(lambda x: int(x),op))
		op,a,b,c = op
		opCode = codeMap[op]
		register = operate(opCode,a,b,c,register)
	return register

if __name__ == '__main__':
	sample = open(part1,'r').readlines()
	ins = readInput(sample)
	print(sumBehaviors(ins,3))
	codeMap = determineOpCodes(ins)
	ops = open(part2,'r').readlines()
	ops = list(map(lambda x: x.strip().split(' '),ops))
	reg = runOps(ops,codeMap)
	print(reg)

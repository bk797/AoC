import sys
sys.path.append('shared/')
from op import operate

file = '../inputs/day19.txt'

#interprets the input into opcodes and determines the instruction pointer register
def readLines(lines):
	ip = int(lines[0].split(' ')[-1])
	ops = []
	for line in lines[1:]:
		opCode,a,b,c = line.split(' ')
		ops.append([opCode,int(a),int(b),int(c)])
	return (ip,ops)

'''
	runs the initializing part of the instructions by operation, but runs the shortened version of the loop
	provided by the abridgedOps
'''
def instructionOps(ip,ops,register):
	count = 1
	while register[ip] != 3:
		index = register[ip]
		register = operate(*ops[index],register)
		print(ops[index],register)
		if index == 2:
			register[3] = register[4]
		register[ip] += 1
		count += 1
	return abridgedOps(register)

'''
	optimizes loop in the instructions
	basically the loop worked like this
	initialize reg[3] and reg[5] to 1
	while reg[5] < reg[4]:
		while reg[3] < reg[4]:
			if reg[3] * reg[5] == reg[4]:
				reg[0] += reg[5]
			reg[3] += 1
		reg[5] += 1
		reg[3] = 1
	in short, what this did was sum all of the factors of reg[4] to reg[0]
	so the loop below iterates reg[5] from 1 to reg[4]'s value and adds reg[5] to reg[0]
	when reg[5] can be divided into reg[4].
	Overall, this reduces the double loop into one loop.
'''
def abridgedOps(register):
	while register[5] <= register[4]:
		if register[4] % register[5] == 0:
			register[0] += register[5]
		register[5] += 1
	return register

if __name__ == '__main__':
	lines = open(file,'r').readlines()
	inputs = readLines(lines)
	part1Register = [0,0,0,0,0,0]
	print(instructionOps(*inputs,part1Register))
	part2Register = [1,0,0,0,0,0]
	print(instructionOps(*inputs,part2Register))

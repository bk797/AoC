import operator

'''
	As the input has a very slow loop in it, I decided to simulate the opcodes in python
	without the loop values
	Then I noticed when checking whether to exit, it will check whether register 4 is equal to register 0
	Part 1) 
		Find the value of register 4 the first time the opcodes go to the exit check
	Part 2)
		Store each value of register 4 that apperas on the exit check until a repeat value shows up, then return
		 the value before the repeat
'''

def emulate():
	vals = {}
	count = 0
	reg = [0,0,0,65536,10552971,0]
	while True:
		reg = l2(reg)
		if 256 > reg[3]:
			# print("check",reg)
			if reg[4] in vals:
				part2 = max(vals.items(), key=operator.itemgetter(1))[0]
				return (part1,part2)
			else:
				if count == 0:
					part1 = reg[4]
				vals[reg[4]] = count
				count += 1
				reg = l5(reg)
				# print(reg[4])
		else:
			# print("l3",reg)
			reg = l3(reg)

def l2(reg):
	reg[5] = reg[3] & 255
	reg[4] += reg[5]
	reg[4] = reg[4] & 16777215
	reg[4] *= 65899
	reg[4] = reg[4] & 16777215
	return reg
	
def l3(reg):
	reg[5] = reg[3] // 256
	reg[2] = 1
	reg[3] = reg[5]
	return reg

def l5(reg):
	reg[3] = reg[4] | 65536
	reg[4] = 10552971
	return reg

if __name__ == '__main__':
	print(emulate())


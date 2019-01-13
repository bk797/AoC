'''
	runs op with given operation function
	when 'r' is invoked, want to make sure that the register is inside range of registers, else throws an exception
'''
def op(func,type,a,b,c,reg):
	n = len(reg)
	reg = reg.copy()
	if type == 'rr':
		if a < n and b < n:
			return func(reg[a],reg[b],c,reg)
	if type == 'ri':
		if a < n:
			return func(reg[a],b,c,reg)
	if type == 'ii':
		return func(a,b,c,reg)
	if type == 'ir':
		if b < n:
			return func(a,reg[b],c,reg)
	else:
		raise Exception

'''
  functions of each operation
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

# runs the provided instruction on the provided register
def operate(opCode,a,b,c,reg):
	if 'add' in opCode:
		return op(add,'r'+opCode[-1],a,b,c,reg)
	elif 'mul' in opCode:
		return op(mul,'r'+opCode[-1],a,b,c,reg)
	elif 'ban' in opCode:
		return op(ban,'r'+opCode[-1],a,b,c,reg)
	elif 'bor' in opCode:
		return op(bor,'r'+opCode[-1],a,b,c,reg)
	elif 'set' in opCode:
		return op(ass,opCode[-1]+'i',a,b,c,reg)
	elif 'gt' in opCode:
		return op(gt,opCode[-2:],a,b,c,reg)
	elif 'eq' in opCode:
		return op(eq,opCode[-2:],a,b,c,reg)

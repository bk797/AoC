from enum import Enum
file = '../inputs/day13.txt'
write = './tracks.txt'
sample = '../inputs/sample.txt'

TRACK_CHARS = "-|+/\\"
CART_CHARS = "<^>v"

class TrackType(Enum):
	horizontal = '-'
	vertical = '|'
	curveA = '/'  #/
	curveB = '\\' #\
	intersection = '+'

class Turn(Enum):
	left = 0
	straight = 1
	right = 2

'''
	Each track stores the type of track and whether a cart is on the track
'''
class Track():

	def __init__(self,char):
		if char in CART_CHARS:
			self.type = cartToTrack(char)
		else:
			self.type = TrackType(char)
		self.cart = None #cart currently occupying the track

'''
	The cart deals with moving the position and movement of the cart
	and keeps track of whether the cart has crashed or not
'''
class Cart:

	def __init__(self,pos,dir):
		self.pos = pos
		self.dir = dir
		self.turn = Turn(0)
		self.crashed = False
	
	#convert direction symbol to coordinates
	def getDir(dir):
		if dir is 'v':
			return (1,0)
		elif dir is '^':
			return (-1,0)
		elif dir is '>':
			return (0,1)
		else:
			return (0,-1)

	#sets the direction arrow of a cart based on the track it is in
	def setDir(self,trackType):
		if trackType is TrackType.curveA: #/
			if self.dir is '>':
				self.dir = '^'
			elif self.dir is '<':
				self.dir = 'v'
			elif self.dir is '^':
				self.dir = '>'
			else:
				self.dir = '<'
		elif trackType is TrackType.curveB: #\
			if self.dir is '<':
				self.dir = '^'
			elif self.dir is '>':
				self.dir = 'v'
			elif self.dir is '^':
				self.dir = '<'
			else:
				self.dir = '>'
		elif trackType is TrackType.intersection:
			cIndex = CART_CHARS.index(self.dir)
			if self.turn is Turn.left:
				self.dir = CART_CHARS[cIndex-1]
			elif self.turn is Turn.right:
				self.dir = CART_CHARS[(cIndex+1) % len(CART_CHARS)]
			self.turn = Turn((self.turn.value + 1) % 3)

	#move the cart by the given direction
	def move(self):
		dir = Cart.getDir(self.dir)
		self.pos = (self.pos[0]+dir[0],self.pos[1]+dir[1])

	#for debugging purposes
	def toString(self):
		pos = self.pos
		dir = self.dir
		return 'pos:%d,%d dir:%s' %(pos[0],pos[1],self.dir)

'''
	The path stores the track and the carts and moves the carts along the track
'''
class Path:

	def __init__(self,tracks,carts):
		self.tracks = tracks
		self.carts = carts
		self.collision = None

	#sort the carts from top to bottom, left to right
	def orderCarts(self):
		self.carts.sort(key=lambda x: x.pos,reverse = False)

	#clear the crashed carts, and move again
	def moveCarts(self):
		self.orderCarts()
		for c in self.carts:
			if not c.crashed:
				self.unoccupyTrack(*c.pos) #check if this actually works
				c.move()
				self.placeCart(c)

	#remove all of the crashed carts in the list of carts
	def clearCrashed(self):
		toRemove = []
		for i in range(0, len(self.carts)):
			c = self.carts[i]
			if c.crashed:
				toRemove.append(i)
		#remove multiple indices from a list at once
		#I wnated to use the sort function so I chose a list over a dict
		self.carts = [i for j, i in enumerate(self.carts) if j not in toRemove]


	#return the first collision
	def findCollision(self):
		n = len(self.carts)
		while len(self.carts) is n:
			self.moveCarts()
			self.clearCrashed()
		return self.collision

	#get the
	def getLastCart(self):
		while len(self.carts) > 1:
			self.moveCarts()
			self.clearCrashed()
		return self.carts[0]

	#added this function so that I could get track by using getTrack(*cart.pos)
	def getTrack(self,col,row):
		return self.tracks[col][row]

	#remove cart from Track
	def unoccupyTrack(self,col,row):
		self.tracks[col][row].cart = None

	#place cart at its given position
	def placeCart(self,cart):
		track = self.getTrack(*cart.pos)
		if track.cart is not None:
			self.collision = cart.pos
			track.cart.crashed = True
			cart.crashed = True
			track.cart = None #instantly remove carts
		else:
			track.cart = cart
			cart.setDir(track.type)

	#a function to write the stored track to a file to make sure that I printed the correct track
	def writeTrack(self):
		writer = open(write,'w')
		row = 0
		line = '   '
		for i in range(0,150):
			line += '%d'%(i%10)
		writer.write(line+'\n')
		for j in  self.tracks:
			col = self.tracks[j]
			line = f'{row:03}'
			for i in range(0,160):
				if i not in col:
					line += ' '
				else:
					line += col[i].type.value
			writer.write(line.strip()+'\n')
			row += 1
		writer.close()


#gets the track underneath the cart (assumes not on intersection or curve)
def cartToTrack(cart):
	if cart is '>' or cart is '<':
		return TrackType.horizontal
	else:
		return TrackType.vertical

#gets the track and carts for a given input
def getPath(lines):
	tracks = {}
	carts = []
	col = 0
	for line in lines:
		tracks[col] = {}
		for row in range(0,len(line)):
			val = line[row]
			if val in TRACK_CHARS:
				tracks[col][row] = Track(val)
			elif val in CART_CHARS:
				tracks[col][row] = Track(val)
				cart = Cart((col,row),val)
				tracks[col][row].cart = cart
				carts.append(cart)
		col += 1
	return Path(tracks,carts)

if __name__ == '__main__':
	track = open(file,'r').readlines()
	# track = open(sample,'r').readlines()
	path = getPath(track)
	print(path.findCollision()) #part 1
	print(path.getLastCart().pos) # part 2
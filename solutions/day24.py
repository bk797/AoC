file = '../inputs/day24.txt'
import math

class Damage:

	def __init__(self,type,amount):
		self.type = type
		self.amount = int(amount)

class Unit:

	def __init__(self,index,unitCount,hitPoints,damage,initiative,weakness=[],immunity=[]):
		self.index = index
		self.unitCount = int(unitCount)
		self.hitPoints = int(hitPoints)
		self.damage = damage
		self.initiative = int(initiative)
		self.weakness = weakness
		self.immunity = immunity
		self.alive = True

	def calcDamage(self,damage):
		dmg = damage.amount
		if damage.type in self.immunity:
			dmg = 0
		elif damage.type in self.weakness:
			dmg *= 2
		return dmg
		
	def takeDamage(self,dmg):
		self.unitCount -= dmg//self.hitPoints
		if self.unitCount < 1:
			self.alive = False

	def effectivePower(self):
		return self.unitCount * self.damage.amount

	def effectiveDamage(self):
		return Damage(self.damage.type,self.effectivePower())

	def __str__(self):
		return "%d,%d,%d"%(self.unitCount,self.initiative,self.index)

class Army:

	def __init__(self,units):
		self.unselected = units
		self.selected = []
		self.dead = []

	def targetUnit(self,unit):
		self.selected.append(unit)
		self.unselected.remove(unit)

	def checkForDead(self):
		for u in self.selected:
			if not u.alive:
				self.selected.remove(u)
				self.dead.append(u)

	def active(self):
		active = self.unselected + self.selected
		active.sort(key=lambda x: x.index, reverse=False)
		return active

	def deselectAll(self):
		self.unselected += self.selected
		self.selected = []

	def reorder(self):
		self.unselected.sort(key=lambda x: x.index, reverse=False)

	def __str__(self):
		s = ""
		for unit in self.active():
			s += unit.__str__() + ","
		return s

def chooseTarget(unit,enemies):
	maxDamage = -1
	enemy = None
	for e in enemies:
		dmg = e.calcDamage(unit.damage)
		if dmg == maxDamage:
			if e.effectivePower() == enemy.effectivePower() and e.initiative > enemy.initiative:
				enemy = e
			elif e.effectivePower() > enemy.effectivePower():
				enemy = e
		elif dmg > maxDamage:
			enemy = e
			maxDamage = dmg
	return enemy

# create a Unit from a line of input
def createUnit(line,index):
	unitsAndHitPoints,weaknessImmunityDmgAndInit = line.split("points")
	units,hitPoints = [unitsAndHitPoints.split(" ")[x] for x in (0,4)]
	if  "(" not in weaknessImmunityDmgAndInit:
		dmg,dmgType,init = [weaknessImmunityDmgAndInit.split(" ")[x] for x in (6,7,-1)]
		weakness = []
		immunity = []
	else:
		weaknessAndImmunity,dmgAndInit = weaknessImmunityDmgAndInit.split(")")
		weakness,immunity = findWeaknessAndImmunity(weaknessAndImmunity)
		dmg,dmgType,init = [dmgAndInit.split(" ")[x] for x in (6,7,-1)]
	return Unit(index,units,hitPoints,Damage(dmgType,dmg),init,weakness,immunity)

# finds eaknesses and immunities from string
# seprate method used as order of weakness and immunity are arbitrary
def findWeaknessAndImmunity(string):
	parts = string.split(";")
	weakness = []
	immunity = []
	for p in parts:
		if "weak" in p:
			weakness = p.replace(",","").split(" ")[3:]
		else:
			immunity = p.replace(",","").split(" ")[3:]
	return (weakness,immunity)

def buildArmies(lines):
	immune = []
	infection = []
	index = 1
	flag = False
	while index < len(lines):
		line = lines[index]
		# print(line)
		if line == '\n':
			index += 2
			flag = True
		else:
			if flag:
				infection.append(createUnit(line,index))
			else:
				immune.append(createUnit(line,index))
			index += 1
	return (Army(immune),Army(infection))

def round(army1,army2):
	# print("ROUND!")
	targetChart = {}
	for unit in army1.active():
		target = chooseTarget(unit,army2.unselected)
		if target is not None:
			army2.targetUnit(target)
			targetChart[unit] = target
	for unit in army2.active():
		target = chooseTarget(unit,army1.unselected)
		if target is not None:
			army1.targetUnit(target)
			targetChart[unit] = target
	units = list(targetChart.keys())
	units.sort(key=lambda x: x.initiative,reverse=True)
	for unit in units:
		# print("select",unit)
		if unit.alive:
			target = targetChart[unit]
			# print("damage",target,target.calcDamage(unit.effectiveDamage()))
			target.takeDamage(target.calcDamage(unit.effectiveDamage()))
	# print(damageChart)
	army1.checkForDead()
	army2.checkForDead()
	army1.deselectAll()
	army2.deselectAll()
	army1.reorder()
	army2.reorder()

def fight(army1,army2):
	army1.reorder()
	army2.reorder()
	while len(army1.unselected) > 0 and len(army2.unselected) > 0:
		round(army1,army2)
		# print("army1",army1)
		# print("army2",army2)
	army = army1 if len(army1.unselected) > 0 else army2
	sum = 0
	for unit in army.unselected:
		sum += unit.unitCount
	return sum

if __name__ == '__main__':
	lines = open(file,'r').readlines()
	armies = buildArmies(lines)
	print(fight(*armies))
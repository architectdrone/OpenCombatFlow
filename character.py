#Open Combat Flow
import dice
import math

class Character():
	HP = 1 #Just so that the character doesn't instantly die.
	effects = {} #A dictionary of effects. We start with no effects.
	position = [0, 0, 0] #Position is a list object so that it can be easily modified.
	groups = [] #Groups of characters. These are specifed as strings. EX: "Enemies", "Undead", etc.
	name = "Set" #A bit of a pun, as the name Set is a name from the Bible.

	#Things to implement in derived classes.
	def getActionBlock(self):
		'''Returns a selected inter-personal action. If the chosen action is not interpersonal, a blank dict will be returned.
		This is a placeholder, and should be implemented in a derived class.'''

		raise NotImplementedError
	
	def getReactionBlock(self, action):
		'''Returns a selected reaction. If the chosen action is not interpersonal, a blank dict will be returned.
		This is a placeholder, and should be implemented in a derived class.'''

		raise NotImplementedError

	def preTurn(self):
		'''This method is called before _update. It doesn't need to be implemented, but it might help with things like status effects.'''

		pass
	
	def postTurn(self):
		'''This method is called at the very end of the turn. It doesn't need to be implemented.'''

		pass
	
	#Getters/Setters
	def setPosition(self, x, y=None, z=None):
		'''Sets the position. Specify however many coordinates you need, up to 3.'''
		self.position[0] = x
		if y is not None:
			self.position[1] = y
		if z is not None:
			self.position[2] = z
	
	def isDead(self):
		'''Returns true if HP <= 0, False otherwise.'''
		if self.HP > 0:
			return False
		else:
			return True

	#Private Methods
	def _update(self):
		'''PRIVATE: Updates status effects, and any other general character things to complete before the turn starts.'''

		#Tick down status effects.
		for effect in self.effects: #Loop through all keys in effects.
			self.effects[effect]-=1 #Decrement the count for each.
			if self.effects[effect] <= 0: #If the counter is less than 0
				self.effects.pop(effect, None) #Remove effects whose counter value is 0.

	def _takeDamage(self, damageBlock):
		'''PRIVATE: Causes character to take the amount of damage specified by the damageBlock, along with all status effects.'''
		
		#Take damage.
		if "damageTaken" in damageBlock:
			self.HP-=damageBlock['damageTaken']
			if self.HP < 0: #Enforce that HP must be >=0
				self.HP = 0
		
		#Take status effects
		if "effects" in damageBlock:
			for effect in damageBlock['effects']: #Look at each effect that was applied by the damageBlock
				if effect in self.effects: #If we already have the effect active.
					self.effects[effect]+=damageBlock['effects'][effect] #Add the amount of time that the effect should be active to the amount of time that is currently active.
				else:
					self.effects[effect]=damageBlock['effects'][effect] #If the effect is not active, we add the effect and set it to the given duration.
		
	def _inRange(self, rangeBlock):
		'''PRIVATE: Returns true if the character is in a certain range.'''

		#Check if the range is empty
		if rangeBlock == {}:
			return False

		#Do area filtering
		if "center" in rangeBlock and "distance" in rangeBlock: #If center and distance are BOTH present.
			#Compute distance
			x1 = self.position[0]
			y1 = self.position[1]
			z1 = self.position[2]
			x2 = rangeBlock['center'][0]
			y2 = (0, rangeBlock['center'][1])[len(rangeBlock['center'])>=2] #Ternary statement that says if the second element of center exists, use it, otherwise use 0.
			z2 = (0, rangeBlock['center'][2])[len(rangeBlock['center'])==3] #See above.
			dist = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)

			#Compare Distances
			if dist > rangeBlock['distance']: #If the distance between points is greater than the specified distance, 
				return False

		#Do group filtering
		if "group" in rangeBlock: #Test if the key 'group' exists in rangeBlock.
			if rangeBlock['group'] not in self.groups: #See if we are part of the requested group. If we are, we hould have a string that is the same as the one specified.
				return False

		#Do character filtering
		if "character" in rangeBlock:
			if rangeBlock['character'] != self:
				return False

		return True

class combatHandler():
	alive = [] #Characters, in combat, who have not yet died
	dead = [] #Characters, in combat, (meaning those who have not yet despawned, and may still be looted), who have died.
	currentCharacterIndex = 0 #The index of the current character within alive
	
	def turn(self):
		'''Executes the turn of the current character.'''
		
		#Get the actor (character executing actions)
		actor = self.alive[self.currentCharacterIndex] #The character executing the action.

		#Do additional things, which do not relate to getting actions.
		actor.preTurn()
		actor._update()

		#Get, and execute, the desired action.
		action = actor.getActionBlock()
		self._executeActionBlock(action)
		
		#Do one more additional thing.
		actor.postTurn()

		#Go to the next character.
		self.currentCharacterIndex+=1
		if self.currentCharacterIndex >= len(self.alive):
			self.currentCharacterIndex = 0
		
	def addCharacter(self, character):
		self.alive.append(character)
	
	def _executeActionBlock(self, action):
		'''PRIVATE: Executes action.'''
		
		#For each effected character, as determined by their response to the range query, get defense and deal damage
		range = action['range']
		for character in self.alive:
			if character._inRange(range):

				#Chance Handling
				if "chance" in action: #Check if a chance is specified.
					if dice.evaluate(action['chance'], return_bool=True) == False: #What happens if the chance fails
						if "failureCondition" in action: #Check to see if a failure condition is specified. 
							self._executeActionBlock(action['failureCondition']) #Execute the failure condition.
						continue #Do not get a reaction, do not deal damage.
				
				#Gathering reaction and creating damage
				reaction = character.getReactionBlock(self, action) #Get the defensive reaction of the effected character.
				damage = self._getDamageBlock(action, reaction) #Get the damage block representing the damage taken by the character.
				character._takeDamage(damage) #Cause character to take damage

				#Retaliation
				if 'action' in reaction: #Check if an action is specified in the reactionBlock.
					self._executeActionBlock(reaction['action'])

				
	def _getDamageBlock(self, action, reaction):
		'''PRIVATE: Get damage'''
		NO_EFFECTS_ON_0_DAMAGE = True #Whether or not effects should be dealt if 0 damage is dealt.
		
		toReturn = {}

		#Look through each key in action['damage'], and see if the reaction has an associated resistance. If not, add it to the total HP lost. If so, subtract resistance and add it to total HP lost.
		total = 0
		for dType in action['damage']: #Loop through the set of all keys in the damage set.
			if dType in reaction['resistance']: #See if that key is in the resistance.
				total+=max(0, action['damage'][dType]-reaction['resistance'][dType]) #If so, add that to the total (with minimum being 0).
			else:
				total+=action['damage'][dType] #Otherwise, just add the total damage amount 
		toReturn['damageTaken'] = total #Add it to the damageBlock.

		#Handle effects
		if "effects" in action: #Only do this if effects are specified.
			if not (total == 0 and NO_EFFECTS_ON_0_DAMAGE): #Also, only do it if the NO_EFFECTS_ON_0_DAMAGE clause doesn't hold.
				toReturn['effects'] = action['effects'] #Add it to the damage block.
		
		return toReturn

	
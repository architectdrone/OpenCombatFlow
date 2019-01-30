#Open Combat Flow
import dice

class Character():
	def getActionBlock(self):
		'''Returns a selected inter-personal action. If the chosen action is not interpersonal, a blank dict will be returned.'''
		#Not yet implemented due to dictionary structure not being determined.
		return {'error': 'Get Action has not yet been implemented'}
	
	def getReactionBlock(self, action):
		'''Returns a selected reaction. If the chosen action is not interpersonal, a blank dict will be returned.'''
		#Not yet implemented due to dictionary structure not being determined.
		return {'error': 'Get Reaction has not yet been implemented'}
	
	def takeDamage(self, damageBlock):
		'''Causes character to take the amount of damage specified by the damageBlock, along with all status effects.'''
		#Not yet implemented due to dictionary structure not being determined.
		return {'error': 'Cannot take damage.'}
	
	def inRange(self, rangeBlock):
		'''Returns true if the character is in a certain range.'''
		#Not yet implemented due to dictionary structure not being determined.
		return False

class combatHandler():
	alive = [] #Characters, in combat, who have not yet died
	dead = [] #Characters, in combat, (meaning those who have not yet despawned, and may still be looted), who have died.
	currentCharacterIndex = 0 #The index of the current character within alive
	
	def turn(self):
		'''Executes the turn of the current character.'''
		
		#Get the actor (character executing actions)
		actor = self.alive[self.currentCharacterIndex] #The character executing the action.
		action = actor.getActionBlock()
		self._executeActionBlock(action)
		
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
			if character.inRange(range):

				#Chance Handling
				if "chance" in action: #Check if a chance is specified.
					if dice.evaluate(action['chance'], return_bool=True) == False: #What happens if the chance fails
						if "failureCondition" in action: #Check to see if a failure condition is specified. 
							self._executeActionBlock(action['failureCondition']) #Execute the failure condition.
						continue #Do not get a reaction, do not deal damage.
				
				#Gathering reaction and creating damage
				reaction = character.getReactionBlock(self, action) #Get the defensive reaction of the effected character.
				damage = self._getDamageBlock(action, reaction) #Get the damage block representing the damage taken by the character.
				character.takeDamage(damage) #Cause character to take damage

				#Retaliation
				if 'action' in reaction: #Check if an action is specified in the reactionBlock.
					self._executeActionBlock(reaction['action'])

				
	def _getDamageBlock(self, action, reaction):
		'''Get damage'''
		NO_EFFECTS_ON_0_DAMAGE = True #Whether or not effects should be dealt if 0 damage is dealt.
		
		toReturn = {}

		#Look through each key in action['damage'], and see if the reaction has an associated resistance. If not, add it to the total HP lost. If so, subtract resistance and add it to total HP lost.
		total = 0
		for dType in action['damage']:
			if dType in reaction['resistance']:
				total+=max(0, action['damage'][dType]-reaction['resistance'][dType])
			else:
				total+=action['damage'][dType]
		toReturn['damageTaken'] = total

		if "effects" in action:
			if not (total == 0 and NO_EFFECTS_ON_0_DAMAGE):
				toReturn['effects'] = action['effects']
		
		return toReturn

	
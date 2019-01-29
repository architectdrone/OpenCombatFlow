import random

def roll(to_roll):
	'''Pass in a string which contains only a dice statement (to_roll), and return a number consistent with the query.'''
	numberDice = int(to_roll.split('d')[0])
	numberSides = int(to_roll.split('d')[1])
	
	total = 0
	for i in range(abs(numberDice)):
		total+=random.randrange(1, numberSides+1)
	
	if numberDice < 0: #If there was a negative number of dice.
		return -1*total
	
	return total
	
def _evaluateHelper(to_eval):
	'''Pass in a string containing any dice string, except those containing a condition (to_eval), and return a number consistent with the query.'''

	#Convert all "-" into "+-"
	to_eval_ready = 
	pass
def evaluate(to_eval, return_bool = False):
	pass
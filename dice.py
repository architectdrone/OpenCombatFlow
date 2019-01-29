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
	to_eval_ready = "+-".join(to_eval.split('-'))

	#Evaluate the new string.
	total = 0
	for statement in to_eval_ready.split('+'):
		#See if the statement is a dice statement, by testing if there is a 'd' in it.
		if "d" in statement:
			total+=roll(statement)
		else: #Otherwise, we assume that it is a constant.
			total+=int(statement)
	return total
	
def evaluate(to_eval, return_bool = False, failure_value = 0):
	'''Evaluate a dice string, and return a number consistent with the query.
	return_bool: Set this to true to return a boolean value instead of a number.
	failure_value: The value to return on a failure.
	'''
	
	if ">" in to_eval:
		condChar = ">"
	elif "<" in to_eval:
		condChar = "<"
	elif "=" in to_eval:
		condChar = "="
	else:
		if return_bool:
			return True
		else:
			return _evaluateHelper(to_eval)

	#Get values before and after the conditional.
	pre = _evaluateHelper(to_eval.split(condChar)[0])
	suf = _evaluateHelper(to_eval.split(condChar)[1])

	#Return an appropriate value based upon the conditional and the value of pre and suf.
	if condChar == ">":
		if pre > suf:
			if return_bool:
				return True
			else:
				return pre
		else:
			if return_bool:
				return False
			else:
				return failure_value
	elif condChar == "<":
		if pre < suf:
			if return_bool:
				return True
			else:
				return pre
		else:
			if return_bool:
				return False
			else:
				return failure_value
	elif condChar == "=":
		if pre == suf:
			if return_bool:
				return True
			else:
				return pre
		else:
			if return_bool:
				return False
			else:
				return failure_value

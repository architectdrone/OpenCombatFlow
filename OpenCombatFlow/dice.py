'''
Open Combat Flow - dice.py
@purpose Evaluates dice strings, using the evaluate() function.
@author Owen Mellema
@date 2-25-19
'''
import random
#See DiceStringFormat.txt for how to use dice strings.
def _roll(to_roll):
	'''
	Pass in a string which contains only a dice statement (to_roll), and return a number consistent with the query.
	@param to_roll A dice string in the form "XdY", where X and Y are integers. Note that X may be negative, but Y cannot be. (How would tht work?)
	@return The result of rolling the dice.
	'''
	numberDice = int(to_roll.split('d')[0])
	numberSides = int(to_roll.split('d')[1])
	
	total = 0
	for i in range(abs(numberDice)):
		total+=random.randrange(1, numberSides+1)
	
	if numberDice < 0: #If there was a negative number of dice.
		return -1*total
	
	return total
	
def _evaluateHelper(to_eval):
	'''
	PRIVATE: A Helper function for evaluating dice strings.
	@param to_eval A dice string with no conditionals.
	@return the result of rolling the dice.
	'''
	
	#Convert all "-" into "+-"
	to_eval_ready = "+-".join(to_eval.split('-'))

	#Evaluate the new string.
	total = 0
	for statement in to_eval_ready.split('+'):
		#See if the statement is a dice statement, by testing if there is a 'd' in it.
		if "d" in statement:
			total+=_roll(statement)
		elif statement == "":
			pass
		else: #Otherwise, we assume that it is a constant.
			total+=int(statement)
	return total
	
def evaluate(to_eval, return_bool = False, failure_value = 0):
	'''
	Evaluate a dice string, and return a number consistent with the query (IE, roll the dice)
	@param to_eval The dice string to be evaluated. If this is an int, it will be returned with nothing else being done
	@param return_bool Set this to true to return a boolean value instead of a number.
	@param failure_value The value to return on a failure.
	@return The result of rolling the dice.
	'''
	
	if type(to_eval)==int:
		return to_eval

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


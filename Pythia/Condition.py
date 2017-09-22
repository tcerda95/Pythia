
def trueCondition(worldState):
	return True

def anyCondition(conditions):
	def anyConditionFunction(worldState):
		for c in conditions:
			if c(worldState):
				return True
		return False
	return anyConditionFunction

def allCondition(conditions):
	def allConditionFunction(worldState):
		for c in conditions:
			if not c(worldState):
				return False
		return True
	return allConditionFunction

def soundCondition(soundState):
	def soundConditionFunction(worldState):
		return worldState.sound == soundState
	return soundConditionFunction

def proximityCondition(proximityState):
	def proximityCondictionFunction(worldState):
		return worldState.proximity == proximityState
	return proximityCondictionFunction
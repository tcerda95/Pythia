
def trueCondition(worldState):
    """Condition that is always true"""
    return True


def anyCondition(conditions):
    """Given a list of conditions it returns a condition which is true when any of the given conditions are true"""
    def anyConditionFunction(worldState):
        for c in conditions:
            if c(worldState):
                return True
        return False
    return anyConditionFunction


def allCondition(conditions):
    """Given a list of conditions it returns a condition which is true when all of the given conditions are true"""
    def allConditionFunction(worldState):
        for c in conditions:
            if not c(worldState):
                return False
        return True
    return allConditionFunction


def soundCondition(soundState):
    """Given a sound state it returns a condition which is true when the world state sound is like the given sound state"""
    def soundConditionFunction(worldState):
        return worldState.sound == soundState
    return soundConditionFunction


def proximityCondition(proximityState):
    """Given a sound state it returns a condition which is true when the world state sound is like the given sound state"""
    def proximityCondictionFunction(worldState):
        return worldState.proximity == proximityState
    return proximityCondictionFunction


def heartbeatCountCondition(count):
    """Given a heartbeat count it returns a condition which is true when the number of successive heartbeats is as given"""
    def heartbeatCountConditionFunction(worldState):
        return worldState.heartbeatCount == count
    return heartbeatCountConditionFunction

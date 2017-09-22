
import Condition


class MachineState:

    def __init__(self, initialState):
        self.transitions = {}
        self.state = initialState
        self.stateSet = {initialState}

    def addTransition(self, fromState, toState, trigger, action, condition=Condition.trueCondition):
        key = (fromState, trigger)

        self.stateSet.add(fromState)
        self.stateSet.add(toState)
        self.transitions[key] = (toState, action, condition)  # may more descriptive to store a dictionary rather than a tuple

    def run(self, trigger, worldState):
        key = (self.state, trigger)

        worldState.update(trigger)

        if key in self.transitions:
            transition = self.transitions[key]
            self.tryTransition(transition, worldState)

    def tryTransition(self, transition, worldState):
        condition = transition[2]

        if condition(worldState):
            self.performTransition(transition)

    def performTransition(self, transition):
        self.state = transition[0]
        transition[1]()

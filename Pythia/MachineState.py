import Condition


class MachineState:
    """Finite machine state. Accepts transitions from a state to another when a Trigger is given and executes the related Action. 
    Optionally, a Condition about the WorldState may be specificied.

    The states are not explicitly set. Only transitions should be specificied and the states are automatically added to the stateSet.
    A transition consists of the fromState, the toState, the Trigger which triggers such transition, the Action related to the transition and
    an optional Condition about the WorldState which must be true in order to perform the transition.

    Attributes:
        transitions (dict): the transitions mapping. (fromState, trigger) -> [(toState1, action1, condition1), ... , (toStateN, actionN, conditionN)]
        state (str): the current state
        stateSet (set): set of all the registered states
    """

    def __init__(self, initialState):
        """Initiates the machine state with the given initial state.

        Args:
            initialState (str): the initial state of the machine
        """

        self.transitions = {}
        self.state = initialState
        self.stateSet = {initialState}

    def addTransition(self, fromState, toState, trigger, action, condition=Condition.trueCondition):
        """Adds a new transition.

        Args:
            fromState (str): the state from which the transition would be performed
            toState (str): the state of the machine after the transition is performed
            trigger (Trigger): the Trigger which triggers the transition
            action (Action): Action to be executed when the transition is performed. It receives WorldState.
            condition (Condition, optional): defaults to Condition.trueCondition. Condition about the WorldState which must be true. 
        """
        key = (fromState, trigger)

        self.stateSet.add(fromState)
        self.stateSet.add(toState)

        if key not in self.transitions:
            self.transitions[key] = []

        self.transitions[key].append((toState, action, condition))  # may be more descriptive to store a dictionary rather than a tuple

    def run(self, trigger, worldState):
        """Performs a transition with the given Trigger and WorldState. 
        If the current state is not related to the given Trigger or the associated Condition is not met, no transition is performed.
        Additionally, the WorldState is appropiately updated by the given Trigger.

        Args:
            trigger (Trigger): the trigger 
            worldState (WorldState): the current world state
        """
        key = (self.state, trigger)

        worldState.update(trigger)

        if key in self.transitions:
            for t in self.transitions[key]:
                self._tryTransition(t, worldState)

    def _tryTransition(self, transition, worldState):
        condition = transition[2]

        if condition(worldState):
            self._performTransition(transition, worldState)

    def _performTransition(self, transition, worldState):
        self.state = transition[0]
        action = transition[1]
        action(worldState)

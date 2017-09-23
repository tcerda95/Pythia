
class TriggerError(Exception):
    """Raised when a trigger is illegal in current state.

    Attributes:
        state (str): state which received illegal trigger
        trigger (Trigger): the illegal trigger
        shouldBeState (str): state in which it should have gone before illegal trigger
    """

    def __init__(self, state, trigger, shouldBeState):
        self.state = prev
        self.trigger = trigger
        self.shouldBeState = shouldBeState
        self.msg = 'Cannot detect {} in {} state. Should have gone to the {} state previously'.format(trigger, state, shouldBeState)

    def __str__(self):
        return self.msg
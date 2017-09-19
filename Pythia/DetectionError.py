
class DetectionError(Exception):
    """Raised when a detection is illegal in current state.

    Attributes:
        state -- state which received illegal detection
        detection -- the illegal detection
        shouldBeState  -- state in which it should have gone before illegal detection
    """

    def __init__(self, state, detection, shouldBeState):
        self.state = prev
        self.detection = detection
        self.shouldBeState = shouldBeState
        self.msg = 'Cannot detect {} in {} state. Should have gone to the {} state previously'.format(detection, state, shouldBeState)

    def __str__(self):
        return self.msg
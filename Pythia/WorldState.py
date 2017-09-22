from Trigger import Trigger
from Trigger import TriggerCategory


class WorldState:
    """ Represents the current worldState by grouping up the last Triggers sensed """

    def __init__(self):
        self.proximity = Trigger.noOneNear
        self.sound = Trigger.silence

    def update(self, trigger):
        if trigger.category == TriggerCategory.proximity:
            self.proximity = trigger

        elif trigger.category == TriggerCategory.sound:
            self.sound = trigger

        return self

    def __eq__(self, other):
        return self.proximity == other.proximity and self.sound == other.sound

from Trigger import Trigger
from Trigger import TriggerCategory


class WorldState:
    """Represents the current WorldState by grouping up the last proximity and sound Triggers sensed.
        
    Attributes:
        proximity (Trigger): the last proximity Trigger sensed.
        sound (Trigger): the last sound Trigger sensed.
        heartbeatCount (int): number of succesive heartbeats.
        aphorismCount (int): number of succesive aphorisms.
    """

    def __init__(self):
        self.proximity = Trigger.noOneNear
        self.sound = Trigger.silence
        self.heartbeatCount = 0
        self.aphorismCount = 0

    def update(self, trigger):
        """Updates the WorldState given a Trigger."""

        if trigger.category != TriggerCategory.heartbeat:
            self._resetHeartbeatCount()

        if trigger.category == TriggerCategory.proximity:
            self.proximity = trigger

        elif trigger.category == TriggerCategory.sound:
            self.sound = trigger

        elif trigger.category == TriggerCategory.heartbeat:
            self.heartbeatCount += 1

        return self

    def aphorismPlayed(self):
        self.aphorismCount += 1

    def resetAphorismCount(self):
        self.aphorismCount = 0

    def _resetHeartbeatCount(self):
        self.heartbeatCount = 0

    def __eq__(self, other):
        return self.proximity == other.proximity and self.sound == other.sound and self.heartbeatCount == other.heartbeatCount and self.aphorismCount == other.aphorismCount

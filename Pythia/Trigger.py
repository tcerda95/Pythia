
class TriggerCategory:
    pass

TriggerCategory.proximity = 'proximity'
TriggerCategory.sound = 'sound'
TriggerCategory.nothing = 'nothing'
TriggerCategory.pythiaBehaviour = 'Pythia behaviour'

class Trigger:
    def __init__(self, trigger, category):
        self.trigger = trigger.strip()
        self.category = category

    def __str__(self):
        return self.trigger

    def __cmp__(self, other):
        return cmp(self.trigger, other.trigger)

    def __hash__(self):
        return hash(self.trigger)

Trigger.isNear = Trigger('isNear', TriggerCategory.proximity)
Trigger.mayBeNear = Trigger('mayBeNear', TriggerCategory.proximity)
Trigger.noOneNear = Trigger('noOneNear', TriggerCategory.proximity)
Trigger.talking = Trigger('talking', TriggerCategory.sound)
Trigger.silence = Trigger('silence', TriggerCategory.sound)
Trigger.endTransmit = Trigger('endTransmit', TriggerCategory.pythiaBehaviour) # Pythia stopped transmition, e.g. talking or making music
Trigger.nothing = Trigger('', TriggerCategory.nothing) # nothing detected; useful on timeouts

triggerDictionary = {
    'isNear': Trigger.isNear,
    'mayBeNear': Trigger.mayBeNear,
    'noOneNear': Trigger.noOneNear,
    'talking': Trigger.talking,
    'silence': Trigger.silence,
    'endTransmit': Trigger.endTransmit,
    '': Trigger.nothing
}

def __triggerFromString__(cls, string): return triggerDictionary[string]

Trigger.fromString = classmethod(__triggerFromString__)

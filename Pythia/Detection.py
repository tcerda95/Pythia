
class DetectionCategory:
    pass

DetectionCategory.proximity = 'proximity'
DetectionCategory.sound = 'sound'
DetectionCategory.nothing = 'nothing'
DetectionCategory.pythiaBehaviour = 'Pythia behaviour'

class Detection:
    def __init__(self, detection, category):
        self.detection = detection.strip()
        self.category = category

    def __str__(self):
        return self.detection

    def __cmp__(self, other):
        return cmp(self.detection, other.detection)

    def __hash__(self):
        return hash(self.detection)

Detection.isNear = Detection('isNear', DetectionCategory.proximity)
Detection.mayBeNear = Detection('mayBeNear', DetectionCategory.proximity)
Detection.noOneNear = Detection('noOneNear', DetectionCategory.proximity)
Detection.talking = Detection('talking', DetectionCategory.sound)
Detection.silence = Detection('silence', DetectionCategory.sound)
Detection.endTransmit = Detection('endTransmit', DetectionCategory.pythiaBehaviour) # Pythia stopped transmition, e.g. talking or making music
Detection.nothing = Detection('', DetectionCategory.nothing) # nothing detected; useful on timeouts

detectionDictionary = {
    'isNear': Detection.isNear,
    'mayBeNear': Detection.mayBeNear,
    'noOneNear': Detection.noOneNear,
    'talking': Detection.talking,
    'silence': Detection.silence,
    'endTransmit': Detection.endTransmit,
    '': Detection.nothing
}

def __detectionFromString__(cls, string): return detectionDictionary[string]

Detection.fromString = classmethod(__detectionFromString__)

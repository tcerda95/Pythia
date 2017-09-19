from Detection import Detection
from Detection import DetectionCategory


class Surroundings:
    """ Represents the current surroundings by grouping up the last Detections sensed """

    def __init__(self):
        self.proximity = Detection.noOneNear
        self.sound = Detection.silence

    def update(self, detection):
        if detection.category == DetectionCategory.proximity:
            self.proximity = detection

        elif detection.category == DetectionCategory.sound:
            self.sound = detection

        return self

    def __eq__(self, other):
        return self.proximity == other.proximity and self.sound == other.sound

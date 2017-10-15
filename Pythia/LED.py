import random
import struct

class LEDLighter:

    def __init__(self, serial):
        self.serial = serial
        self.leds = set()
        self.ledMap = {}

    def addLedGroup(self, name, *numbers):
        self.ledMap[name] = set(numbers)  # Clone given list

        for n in numbers:
            self.leds.add(n)

        return self

    def lightAllLeds(self):
        self._transmitLeds(self.leds)
        return list(self.leds)

    def lightRandomLeds(self, lightChance=0.5):

        if lightChance < 0.0 or lightChance > 1.0:
            raise Exception('Invalid lightChance: {}. Should be between 0 and 1.0'.format(lightChance))

        lightLeds = [led for led in self.leds if random.random() < lightChance]

        self._transmitLeds(lightLeds)

        return lightLeds

    def lightLedGroups(self, *groups):
        lightLeds = set()

        for g in groups:
            lightLeds = lightLeds.union(self.ledMap[g])

        self._transmitLeds(lightLeds)

        return list(lightLeds)

    def _transmitLeds(self, leds):
        fmt = '>' + 'B' * len(leds)
        self.serial.write(struct.pack(fmt, *leds))

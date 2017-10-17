import random
import struct

class LEDLighter:
    """Manages communication with another device through the Serial required for lighting up LEDs.
    The pin numbers corresponding to the LEDs should be previously configured in groups with the addLedGroup method.
    Once configuration is done, the LEDs may be lit up with the lightAllLeds(), lightRandomLeds() or lightLedGroups() mehtods.
        
    Attributes:
        serial (Serial): the serial from which the other device is listening.
        leds (set): set of pin number corresponding to LEDs which were already setup.
        ledMap (dict): maps the groups names with the corresponding pin numbers.
    """

    def __init__(self, serial):
        """Initiates a LEDLighter instance associate with the given Serial.

        Args:
            serial (Serial): the serial from which the other device is listening.
        """
        self.serial = serial
        self.leds = set()
        self.ledMap = {}

    def addLedGroup(self, name, *numbers):
        """Associates a name with the given pin numbers.

        Args:
            name (str): the name of the LED group.
            *numbers (int): the pin numbers corresponding to the LEDs.

        Returns:
            LedLighter: self.
        """

        self.ledMap[name] = set(numbers)  # Clone given list

        for n in numbers:
            self.leds.add(n)

        return self

    def lightAllLeds(self):
        """Lights up all configured LEDs. These would correspond to the content of self.leds.

        Returns:
            list: the list of lit up LEDs.
        """

        self._transmitLeds(self.leds)
        return list(self.leds)

    def lightRandomLeds(self, lightChance=0.5):
        """Lights up a random sequence of LEDs corresponding to a subset of self.leds with the given possibility.

        Args:
            lightChance (float, optional): defaults to 0.5. Possibility of lighting up each LED. Must be between 0.0 and 1.0.

        Returns:
            list: the list of lit up LEDs.
        """

        if lightChance < 0.0 or lightChance > 1.0:
            raise Exception('Invalid lightChance: {}. Should be between 0 and 1.0'.format(lightChance))

        lightLeds = [led for led in self.leds if random.random() < lightChance]

        self._transmitLeds(lightLeds)

        return lightLeds

    def lightLedGroups(self, *groups):
        """Lights up the LEDs corresponding to the given groups.

        Args:
            *groups (str): the names of the groups which LEDs should be lit up.

        Returns:
            list: the list of lit up LEDs.
        """

        lightLeds = set()

        for g in groups:
            lightLeds = lightLeds.union(self.ledMap[g])

        self._transmitLeds(lightLeds)

        return list(lightLeds)

    def _transmitLeds(self, leds):
        fmt = '>' + 'B' * len(leds)
        self.serial.write(struct.pack(fmt, *leds))

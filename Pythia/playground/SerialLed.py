import serial
import time
from LED import LEDLighter

ser = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=1)  #  1 sec timeout

ledLighter = LEDLighter(ser)

ledLighter.addLedGroup('white', 5)
ledLighter.addLedGroup('blue', 6, 7)
ledLighter.addLedGroup('green', 8, 9)
ledLighter.addLedGroup('yellow', 10, 11)
ledLighter.addLedGroup('red', 12, 13)

while True:
    time.sleep(1)
    ledLighter.lightRandomLeds(0.6)
    time.sleep(1)
    ledLighter.lightLedGroups('white')
    time.sleep(1)
    ledLighter.lightLedGroups('blue')
    time.sleep(1)
    ledLighter.lightLedGroups('green')
    time.sleep(1)
    ledLighter.lightLedGroups('yellow')
    time.sleep(1)
    ledLighter.lightLedGroups('red')
    time.sleep(1)
    ledLighter.lightLedGroups('red', 'yellow', 'green', 'white')
    time.sleep(1)
    ledLighter.lightAllLeds()

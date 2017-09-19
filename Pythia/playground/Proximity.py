import os
import serial
import random
import time

from pygame import mixer

mixer.init()
ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
aforismos = []

for filename in os.listdir('./music'):
    if '.mp3' in filename:
        aforismos.append('music/' + filename)

print aforismos

mixer.music.load(aforismos[0])
mixer.music.play()

try:
    while True:
        state = ser.readline()
        select = -1

        if 'mayBeNear' in state:
            mixer.music.set_volume(0.2)

        elif 'isNear' in state:
            select = random.randint(0, len(aforismos)-1)

        else:
            mixer.music.set_volume(1)

        print state

        if select != -1:
            print 'playing: ', aforismos[select]

            mixer.music.load(aforismos[select])
            mixer.music.set_volume(1)
            mixer.music.play()

except:
    pass
finally:
    pass

print aforismos


import os
import serial
import random
import time

from pygame import mixer

mixer.init()
ser = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout = 5) # 5 secs timeout
aforismos = []

for filename in os.listdir('./music'):
    if '.mp3' in filename:
        aforismos.append('music/' + filename)

print aforismos

mixer.music.load(aforismos[0])
mixer.music.play()

while True:
    state = ser.readline().strip()
    select = -1

#    if 'mayBeNear' in state:
#        mixer.music.set_volume(0.2)

    if 'isNear' in state:
        select = random.randint(0, len(aforismos)-1)

#    elif 'noOneNear' in state:
#        mixer.music.set_volume(1)

    elif 'talking' in state:
        mixer.music.set_volume(0.2)

    elif 'silence' in state:
        mixer.music.set_volume(1)

    print state

    if not mixer.music.get_busy:
        select = random.randint(0, len(aforismos) - 1)

    if select != -1:
        print 'playing: ', aforismos[select]

        mixer.music.load(aforismos[select])
        mixer.music.set_volume(1)
        mixer.music.play()

print aforismos


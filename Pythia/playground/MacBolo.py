import os
import serial
import random
import time

from pygame import mixer

mixer.init()
aforismos = []

for filename in os.listdir('./music'):
    if ".mp3" in filename:
        aforismos.append('music/' + filename)

print aforismos

try:
    while True:
        time.sleep(5)

        select = random.randint(0,len(aforismos)-1)

        print 'playing: ', aforismos[select]

        mixer.music.load(aforismos[select])
        mixer.music.play()
except:
    pass
finally:
    pass


print aforismos


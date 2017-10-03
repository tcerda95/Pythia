import os
import serial
import random
import time

from pygame import mixer

mixer.init()
songs = []

for filename in os.listdir('./music'):
    if ".mp3" in filename:
        songs.append('music/' + filename)

print songs

while True:
    time.sleep(5)

    select = random.randint(0,len(songs)-1)

    print 'playing: ', songs[select]

    mixer.music.load(songs[select])
    mixer.music.play()


print songs


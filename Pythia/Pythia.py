import os
import serial
import random
import time
from Detection import Detection
from State import PythiaState
from Surroundings import Surroundings
import pygame
from pygame import mixer


SONG_END = pygame.USEREVENT + 1
MAX_TIMEOUTS = 5

pygame.init()
mixer.init()
mixer.music.set_endevent(SONG_END)

ser = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=1)  # 1 sec timeout

state = PythiaState.idle
state.run()
surroundings = Surroundings()
timeoutCount = 0


def consumeDetection(state, detection, surroundings):
    surroundings.update(detection)
    prevState = state
    state = state.next(detection, surroundings)

    if prevState is not state:
        timeoutCount = 0
        state.run()

    return state


while True:
    print state
    sense = ser.readline().strip()
    detection = Detection.fromString(sense)

    if detection is Detection.nothing:
        timeoutCount += 1

        if timeoutCount == MAX_TIMEOUTS:
            timeoutCount = 0
            state = consumeDetection(state, detection, surroundings)

    else:
        state = consumeDetection(state, detection, surroundings)

    for event in pygame.event.get():
        if event.type == SONG_END:
            state = consumeDetection(state, Detection.endTransmit, surroundings)

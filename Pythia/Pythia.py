import os
import serial
import random
import time
from Trigger import Trigger
from State import PythiaState
from WorldState import WorldState
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
worldState = WorldState()
timeoutCount = 0


def consumeTrigger(state, trigger, worldState):
    worldState.update(trigger)
    prevState = state
    state = state.next(trigger, worldState)

    if prevState is not state:
        timeoutCount = 0
        state.run()

    return state


while True:
    print state
    sense = ser.readline().strip()
    trigger = Trigger.fromString(sense)

    if trigger is Trigger.nothing:
        timeoutCount += 1

        if timeoutCount == MAX_TIMEOUTS:
            timeoutCount = 0
            state = consumeTrigger(state, trigger, worldState)

    else:
        state = consumeTrigger(state, trigger, worldState)

    for event in pygame.event.get():
        if event.type == SONG_END:
            state = consumeTrigger(state, Trigger.endTransmit, worldState)

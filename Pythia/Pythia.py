import serial
import random
import pygame
import os
from pygame import mixer
from Trigger import Trigger
from WorldState import WorldState
from MachineState import MachineState
import Action
import Condition


SONG_END = pygame.USEREVENT + 1
MAX_TIMEOUTS = 1
REPEAT_SPEECH_HEARTBEATS = 5  # repeats the engage speech after 5 heartbeats of waiting an answer

pygame.init()
mixer.init()
mixer.music.set_endevent(SONG_END)


def soundFiles(directory):
    names = []
    for filename in os.listdir(directory):
        if '.mp3'in filename or '.wav' in filename:
            names.append(directory + '/' + filename)
    print names
    return names

machineState = MachineState('alone')

engageSpeech = Action.playRandomSpeech(soundFiles('engageSpeeches'))
repeatEngage = Action.playRandomSpeech(soundFiles('repeatEngage'))
playAphorism = Action.playRandomSpeech(soundFiles('aphorisms'))
randomMusic = Action.playRandomMusic(soundFiles('music'))

machineState.addTransition('alone', 'notAlone', Trigger.mayBeNear, Action.lowerVolume)
machineState.addTransition('alone', 'alone', Trigger.endTransmit, randomMusic)

machineState.addTransition('notAlone', 'alone', Trigger.noOneNear, Action.higherVolume)
machineState.addTransition('notAlone', 'engage', Trigger.isNear, Action.chain([Action.higherVolume, engageSpeech]))

machineState.addTransition('engage', 'alone', Trigger.noOneNear, randomMusic)  # TODO: disappointed speech
machineState.addTransition('engage', 'waitAnswer', Trigger.endTransmit, Action.doNothing, Condition.soundCondition(Trigger.silence))
machineState.addTransition('engage', 'listen', Trigger.endTransmit, Action.doNothing, Condition.soundCondition(Trigger.talking))

machineState.addTransition('waitAnswer', 'alone', Trigger.noOneNear, randomMusic)   # TODO: disappointed speech
machineState.addTransition('waitAnswer', 'engage', Trigger.heartbeat, repeatEngage, Condition.heartbeatCountCondition(REPEAT_SPEECH_HEARTBEATS))
machineState.addTransition('waitAnswer', 'listen', Trigger.talking, Action.doNothing)

machineState.addTransition('listen', 'alone', Trigger.noOneNear, randomMusic)  # TODO: disappointed speech
machineState.addTransition('listen', 'aphorism', Trigger.silence, playAphorism)

machineState.addTransition('aphorism', 'alone', Trigger.endTransmit, randomMusic, Condition.proximityCondition(Trigger.noOneNear))
machineState.addTransition('aphorism', 'notAlone', Trigger.endTransmit, engageSpeech, Condition.proximityCondition(Trigger.mayBeNear))
machineState.addTransition('aphorism', 'engage', Trigger.endTransmit, engageSpeech, Condition.proximityCondition(Trigger.isNear))


worldState = WorldState()
ser = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=1)  # 1 sec timeout

randomMusic(worldState)

while True:
    print machineState.state
    sense = ser.readline().strip()
    trigger = Trigger.fromString(sense)

    machineState.run(trigger, worldState)

    for event in pygame.event.get():
        if event.type == SONG_END:
            machineState.run(Trigger.endTransmit, worldState)

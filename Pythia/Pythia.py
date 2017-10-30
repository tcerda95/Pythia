import serial
import pygame
import os
from pygame import mixer
from Trigger import Trigger
from WorldState import WorldState
from MachineState import MachineState
from LED import LEDLighter
import Action
import Condition


SONG_END = pygame.USEREVENT + 1
MAX_TIMEOUTS = 1
REPEAT_SPEECH_HEARTBEATS = 10  # repeats the engage speech after given heartbeats of waiting an answer

pygame.init()
mixer.init()
mixer.music.set_endevent(SONG_END)


def soundFiles(directory):
    names = []
    for filename in os.listdir(directory):
        if '.mp3' in filename or '.wav' in filename or '.ogg' in filename:
            names.append(directory + '/' + filename)
    print names
    return names


ser = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=1)  # 1 sec timeout


# LED Setup

ledLighter = LEDLighter(ser)
ledLighter.addLedGroup('white', 5)
ledLighter.addLedGroup('blue', 6, 7)
ledLighter.addLedGroup('green', 8, 9)
ledLighter.addLedGroup('yellow', 10, 11)
ledLighter.addLedGroup('red', 12, 13)


# Actions setup

engageSpeech = Action.playRandomSpeech(soundFiles('engageSpeech'))
angrySpeech = Action.playRandomSpeech(soundFiles('offendedSpeech'))
thankSpeech = Action.playRandomSpeech(soundFiles('thankSpeech'))
repeatEngage = Action.playRandomSpeech(soundFiles('repeatEngage'))
playAphorism = Action.chain([Action.playRandomSpeech(soundFiles('aphorisms')), Action.incrementAphorismCount])
randomMusic = Action.playRandomMusic(soundFiles('music'))

lightRandomLeds = Action.lightRandomLeds(ledLighter)
pythiaTalkingLeds = Action.lightLeds(ledLighter, 'blue', 'green', 'white')
waitAnswerLeds = Action.lightLeds(ledLighter, 'blue')
listenLeds = Action.lightLeds(ledLighter, 'green', 'blue')
attentionLeds = Action.lightLeds(ledLighter, 'red', 'yellow')
offendedLeds = Action.lightLeds(ledLighter, 'red')

offendedAction = Action.chain([offendedLeds, angrySpeech, randomMusic, Action.resetAphorismCount])
standbyAction = Action.chain([lightRandomLeds, randomMusic, Action.resetAphorismCount])
thankfulAction = Action.chain([pythiaTalkingLeds, thankSpeech, randomMusic, Action.resetAphorismCount])
engageAction = Action.chain([pythiaTalkingLeds, engageSpeech])

# Machine State Setup

machineState = MachineState('alone')

machineState.addTransition('alone', 'notAlone', Trigger.mayBeNear, Action.chain([Action.lowerVolume, attentionLeds]))
machineState.addTransition('alone', 'alone', Trigger.endTransmit, randomMusic)
machineState.addTransition('alone', 'alone', Trigger.heartbeat, lightRandomLeds)

machineState.addTransition('notAlone', 'alone', Trigger.noOneNear, Action.chain([Action.higherVolume, standbyAction]))
machineState.addTransition('notAlone', 'engage', Trigger.isNear, Action.chain([Action.higherVolume, engageAction]))

machineState.addTransition('engage', 'alone', Trigger.noOneNear, offendedAction, Condition.noAphorismPlayedCondition)
machineState.addTransition('engage', 'thanking', Trigger.noOneNear, thankfulAction, Condition.aphorismPlayedCondition)
machineState.addTransition('engage', 'waitAnswer', Trigger.endTransmit, waitAnswerLeds, Condition.soundCondition(Trigger.silence))
machineState.addTransition('engage', 'listen', Trigger.endTransmit, listenLeds, Condition.soundCondition(Trigger.talking))

machineState.addTransition('waitAnswer', 'alone', Trigger.noOneNear, offendedAction, Condition.noAphorismPlayedCondition)
machineState.addTransition('waitAnswer', 'thanking', Trigger.noOneNear, thankfulAction, Condition.aphorismPlayedCondition)
machineState.addTransition('waitAnswer', 'engage', Trigger.heartbeat, Action.chain([repeatEngage, pythiaTalkingLeds]), Condition.heartbeatCountCondition(REPEAT_SPEECH_HEARTBEATS))
machineState.addTransition('waitAnswer', 'listen', Trigger.talking, listenLeds)

machineState.addTransition('listen', 'alone', Trigger.noOneNear, offendedAction, Condition.noAphorismPlayedCondition)
machineState.addTransition('listen', 'thanking', Trigger.noOneNear, thankfulAction, Condition.aphorismPlayedCondition)
machineState.addTransition('listen', 'aphorism', Trigger.silence, Action.chain([playAphorism, pythiaTalkingLeds]))

machineState.addTransition('aphorism', 'thanking', Trigger.endTransmit, thankfulAction, Condition.proximityCondition(Trigger.noOneNear))
machineState.addTransition('aphorism', 'notAlone', Trigger.endTransmit, attentionLeds, Condition.proximityCondition(Trigger.mayBeNear))
machineState.addTransition('aphorism', 'engage', Trigger.endTransmit, engageAction, Condition.proximityCondition(Trigger.isNear))

machineState.addTransition('thanking', 'alone', Trigger.endTransmit, standbyAction, Condition.proximityCondition(Trigger.noOneNear))
machineState.addTransition('thanking', 'notAlone', Trigger.endTransmit, attentionLeds, Condition.proximityCondition(Trigger.mayBeNear))
machineState.addTransition('thanking', 'engage', Trigger.endTransmit, engageAction, Condition.proximityCondition(Trigger.isNear))

worldState = WorldState()

standbyAction(worldState)

while True:
    print machineState.state
    sense = ser.readline().strip()
    trigger = Trigger.fromString(sense)

    machineState.run(trigger, worldState)

    for event in pygame.event.get():
        if event.type == SONG_END:
            machineState.run(Trigger.endTransmit, worldState)

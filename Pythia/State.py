from pygame import mixer
from random import shuffle
from Trigger import Trigger
from TriggerError import TriggerError
import os
import random


class PythiaState:
    pass


class IdleState(PythiaState):
    """No one near Pythia. Play some music"""
    def __init__(self, music):
        self.music = music

    def run(self):
        shuffle(self.music)

        if not mixer.music.get_busy():  # play if not already playing
            mixer.music.load(self.music[0])
            mixer.music.play()

        for m in self.music:
            mixer.music.queue(m)

        return self

    def next(self, trigger, worldState):
        if trigger == Trigger.mayBeNear:
            return PythiaState.lowVolume

        elif trigger == Trigger.isNear:
            raise TriggerError(self, trigger, PythiaState.lowVolume)

        elif trigger == Trigger.endTransmit:
            self.run()
            return self

        else:
            return self

    def __str__(self):
        return 'idle'


class LowVolumeState(PythiaState):
    """Someone may be near Pythia. Lower music volume."""
    def run(self):
        mixer.music.set_volume(0.3)
        return self

    def next(self, trigger, worldState):
        if trigger == Trigger.noOneNear:
            mixer.music.set_volume(1)
            return PythiaState.idle

        elif trigger == Trigger.isNear:
            mixer.music.set_volume(1)
            return PythiaState.engage

        elif trigger == Trigger.mayBeNear:
            raise TriggerError(self, trigger, PythiaState.idle)

        else:
            return self

    def __str__(self):
        return 'low volume'


class EngageState(PythiaState):
    """Someone near Pythia. Engage him/her with a presentation speech."""
    def __init__(self, presentations):
        self.presentations = presentations

    def run(self):
        select = random.randint(0, len(self.presentations) - 1)
        mixer.music.load(self.presentations[select])
        mixer.music.play()
        return self

    def next(self, trigger, worldState):
        if trigger == Trigger.endTransmit and worldState.sound == Trigger.talking:
            return PythiaState.listen

        elif trigger == Trigger.endTransmit and worldState.sound == Trigger.silence:
            return PythiaState.waitAnswer

        elif trigger == Trigger.noOneNear:  # TODO: disappointed speech when person leaves during pythia presentation
            return PythiaState.idle

        elif trigger == Trigger.mayBeNear or trigger == Trigger.isNear:
            raise TriggerError(self, trigger, PythiaState.idle)

        else:
            return self

    def __str__(self):
        return 'engage'


class WaitAnswerState(PythiaState):
    """Pythia finished presentation speech. Wait until the person in front starts talking."""
    def run(self):
        return self

    def next(self, trigger, worldState):
        if trigger == Trigger.nothing:  # timeout: repeating presentation
            return PythiaState.engage

        elif trigger == Trigger.noOneNear: # TODO: disappointed speech when person leaves without answering
            return PythiaState.idle

        elif trigger == Trigger.talking:
            return PythiaState.listen

        elif trigger == Trigger.mayBeNear or trigger == Trigger.isNear:
            raise TriggerError(self, trigger, PythiaState.idle)

        elif trigger == Trigger.silence:
            raise TriggerError(self, trigger, PythiaState.listen)

        else:
            return self

    def __str__(self):
        return 'wait answer'


class ListenState(PythiaState):
    """Person in fron Pythia is talking. Listen until it finishes."""
    def run(self):
        return self

    def next(self, trigger, worldState):  
        if trigger == Trigger.noOneNear: # TODO: disappointed speech when person leaves without answering
            return PythiaState.idle

        elif trigger == Trigger.silence:
            return PythiaState.aphorism

        elif trigger == Trigger.talking:
            raise TriggerError(self, trigger, PythiaState.aphorism)

        elif trigger == Trigger.mayBeNear or trigger == Trigger.isNear:
            raise TriggerError(self, trigger, PythiaState.idle)

        else:
            return self

    def __str__(self):
        return 'listen'


class AphorismState(PythiaState):
    """Person finished talking. Play aphorism."""
    def __init__(self, aphorisms):
        self.aphorisms = aphorisms

    def run(self):
        select = random.randint(0, len(self.aphorisms) - 1)
        mixer.music.load(self.aphorisms[select])
        mixer.music.play()
        return self

    def next(self, trigger, worldState):
        if trigger == Trigger.noOneNear:
            return PythiaState.idle

        elif trigger == Trigger.endTransmit:
            return PythiaState.engage

        elif trigger == Trigger.mayBeNear or trigger == Trigger.isNear:
            raise TriggerError(self, trigger, PythiaState.idle)

        else:
            return self

    def __str__(self):
        return 'aphorism'


PythiaState.idle = IdleState(['music/allegro.mp3'])
PythiaState.lowVolume = LowVolumeState()
PythiaState.engage = EngageState(['music/canon.mp3'])
PythiaState.listen = ListenState()
PythiaState.waitAnswer = WaitAnswerState()
PythiaState.aphorism = AphorismState(['music/seasons.mp3'])

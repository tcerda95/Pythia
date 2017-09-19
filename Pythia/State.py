from pygame import mixer
from random import shuffle
from Detection import Detection
from DetectionError import DetectionError
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

    def next(self, detection, surroundings):
        if detection == Detection.mayBeNear:
            return PythiaState.lowVolume

        elif detection == Detection.isNear:
            raise DetectionError(self, detection, PythiaState.lowVolume)

        elif detection == Detection.endTransmit:
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

    def next(self, detection, surroundings):
        if detection == Detection.noOneNear:
            mixer.music.set_volume(1)
            return PythiaState.idle

        elif detection == Detection.isNear:
            mixer.music.set_volume(1)
            return PythiaState.engage

        elif detection == Detection.mayBeNear:
            raise DetectionError(self, detection, PythiaState.idle)

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

    def next(self, detection, surroundings):
        if detection == Detection.endTransmit and surroundings.sound == Detection.talking:
            return PythiaState.listen

        elif detection == Detection.endTransmit and surroundings.sound == Detection.silence:
            return PythiaState.waitAnswer

        elif detection == Detection.noOneNear:  # TODO: disappointed speech when person leaves during pythia presentation
            return PythiaState.idle

        elif detection == Detection.mayBeNear or detection == Detection.isNear:
            raise DetectionError(self, detection, PythiaState.idle)

        else:
            return self

    def __str__(self):
        return 'engage'


class WaitAnswerState(PythiaState):
    """Pythia finished presentation speech. Wait until the person in front starts talking."""
    def run(self):
        return self

    def next(self, detection, surroundings):
        if detection == Detection.nothing:  # timeout: repeating presentation
            return PythiaState.engage

        elif detection == Detection.noOneNear: # TODO: disappointed speech when person leaves without answering
            return PythiaState.idle

        elif detection == Detection.talking:
            return PythiaState.listen

        elif detection == Detection.mayBeNear or detection == Detection.isNear:
            raise DetectionError(self, detection, PythiaState.idle)

        elif detection == Detection.silence:
            raise DetectionError(self, detection, PythiaState.listen)

        else:
            return self

    def __str__(self):
        return 'wait answer'


class ListenState(PythiaState):
    """Person in fron Pythia is talking. Listen until it finishes."""
    def run(self):
        return self

    def next(self, detection, surroundings):  
        if detection == Detection.noOneNear: # TODO: disappointed speech when person leaves without answering
            return PythiaState.idle

        elif detection == Detection.silence:
            return PythiaState.aphorism

        elif detection == Detection.talking:
            raise DetectionError(self, detection, PythiaState.aphorism)

        elif detection == Detection.mayBeNear or detection == Detection.isNear:
            raise DetectionError(self, detection, PythiaState.idle)

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

    def next(self, detection, surroundings):
        if detection == Detection.noOneNear:
            return PythiaState.idle

        elif detection == Detection.endTransmit:
            return PythiaState.engage

        elif detection == Detection.mayBeNear or detection == Detection.isNear:
            raise DetectionError(self, detection, PythiaState.idle)

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

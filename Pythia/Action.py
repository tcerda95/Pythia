from pygame import mixer
import random


def chain(actions):
    """Given a list of actions it returns an action that performs each given action in successive order"""
    def chainFunction(worldState):
        for a in actions:
            a(worldState)
    return chainFunction


def playRandomMusic(music):
    def playRandomMusicFunction(worldState):
        random.shuffle(music)

        if not mixer.music.get_busy():  # play if not already playing
            mixer.music.load(music[0])
            mixer.music.play()

        for m in music:
            mixer.music.queue(m)

    return playRandomMusicFunction


def lowerVolume(worldState):
    mixer.music.set_volume(0.3)


def higherVolume(worldState):
    mixer.music.set_volume(1)


def playRandomSpeech(speeches):
    def playSpeechFunction(worldState):
        select = random.randint(0, len(speeches) - 1)
        mixer.music.load(speeches[select])
        mixer.music.play()
    return playSpeechFunction


def lightLeds(ledLighter, *groups):
    def lightLedsFunction(worldState):
        ledLighter.lightLedGroups(*groups)
    return lightLedsFunction


def lightRandomLeds(ledLighter):
    def lightRandomLedsFunction(worldState):
        ledLighter.lightRandomLeds()
    return lightRandomLedsFunction


def doNothing(worldState):
    pass

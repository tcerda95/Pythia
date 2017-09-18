#include "TalkingSensor.h"

/* How many times the pin would be read for sound signals */
#define LISTEN_TRIES 20

TalkingSensor::TalkingSensor(int digitalPin, int talkingThreshold) {
  pinMode(digitalPin, INPUT);
  _pin = digitalPin;
  _talkingThreshold = talkingThreshold;
  _timeSinceLastSound = 0;
}

/*
 * Returns true if someone is talking, false otherwise.
 * The talking threshold time must be surprassed with
 * no sound in order to return false.
 */
bool TalkingSensor::isTalking() {
  int sound;

  for (int i = 0; i < LISTEN_TRIES; i++) {
      sound = digitalRead(_pin);
      if (sound == HIGH)
        _timeSinceLastSound = 0;
      delay(1);
  }

  return _timeSinceLastSound <= _talkingThreshold;
}

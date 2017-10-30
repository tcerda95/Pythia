#include "TalkingSensor.h"

/* How many times the pin would be read for sound signals */
#define LISTEN_TRIES 20000

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
  bool listened = false;

  for (int i = 0; i < LISTEN_TRIES && !listened; i++) {
    sound = digitalRead(_pin);
    if (sound == HIGH) {
      _timeSinceLastSound = 0;
      listened = true;
    }
  }

  return _timeSinceLastSound <= _talkingThreshold;
}

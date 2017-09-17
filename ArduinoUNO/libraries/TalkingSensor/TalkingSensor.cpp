
#include "TalkingSensor.h"

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
  int sound = digitalRead(_pin);

  if (sound == HIGH)
      _timeSinceLastSound = 0;

  return _timeSinceLastSound <= _talkingThreshold;
}

#include <elapsedMillis.h>
#include <NewPing.h>

const int YELLOW = 9;
const int GREEN = 10;
const int RED = 11;
const int MAX_DISTANCE = 125; // in centimeters
const int NEAR_ENOUGH_MILLIS = 1500; // Two seconds
const int TRIGGER = 3;
const int ECHO = 7;

elapsedMillis someoneNearTime;
NewPing sensor(TRIGGER, ECHO, MAX_DISTANCE);

const int leds[] = {RED, YELLOW, GREEN};
const int nLeds = sizeof(leds)/sizeof(leds[0]);

typedef struct proximity {
  int led;
  struct proximity (*callback) (int);
} Proximity;

Proximity noOneNearCallback(int distance);
Proximity mayBeNearCallback(int distance);
Proximity isNearCallback(int distance);

const Proximity noOneNear = {
  RED,
  noOneNearCallback
};

const Proximity mayBeNear = {
  YELLOW,
  mayBeNearCallback
};

const Proximity isNear = {
  GREEN,
  isNearCallback
};

Proximity proximity;

void setup() {
  int i;
  Serial.begin(9600);

  for (i = 0; i < nLeds; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }

  proximity = noOneNear;
  digitalWrite(proximity.led, HIGH);
}

void loop() {
  int distance = sensor.ping_cm();
  int prevLed = proximity.led;
  proximity = proximity.callback(distance);

  if (prevLed != proximity.led) {
    digitalWrite(prevLed, LOW);
    digitalWrite(proximity.led, HIGH);
  }
  
  delay(100);
}


Proximity noOneNearCallback(int distance) {
  if (distance) {
    someoneNearTime = 0;
    return mayBeNear;
  }
  else {
    return noOneNear;
  }
}

Proximity mayBeNearCallback(int distance) {
  if (distance && hasBeenNearEnough())
    return isNear;
  else if (distance)
    return mayBeNear;
  else
    return noOneNear;
}

Proximity isNearCallback(int distance) {
  if (distance)
    return isNear;
  else
    return noOneNear;
}

boolean hasBeenNearEnough() {
  return someoneNearTime > NEAR_ENOUGH_MILLIS;
}

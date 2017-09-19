#include <TalkingSensor.h>
#include <elapsedMillis.h>
#include <NewPing.h>

const int YELLOW = 9;
const int GREEN = 10;
const int RED = 11;
const int MAX_DISTANCE = 125; // in centimeters
const int NEAR_ENOUGH_MILLIS = 1500; // One and a half seconds
const int TRIGGER = 3;
const int ECHO = 7;
const int PINGS = 15;
const int TALKING_SENSOR_PIN = 13;
const int TALK_THRESHOLD = 2500;

elapsedMillis someoneNearTime;
NewPing sensor(TRIGGER, ECHO, MAX_DISTANCE);
TalkingSensor talkingSensor(TALKING_SENSOR_PIN, TALK_THRESHOLD);

const int leds[] = {RED, YELLOW, GREEN};
const int nLeds = sizeof(leds)/sizeof(leds[0]);

typedef struct proximity {
  char * stateName;
  int led;
  struct proximity (*callback) (int);
} Proximity;

Proximity noOneNearCallback(int distance);
Proximity mayBeNearCallback(int distance);
Proximity isNearCallback(int distance);

const Proximity noOneNear = {
  "noOneNear",
  RED,
  noOneNearCallback
};

const Proximity mayBeNear = {
  "mayBeNear",
  YELLOW,
  mayBeNearCallback
};

const Proximity isNear = {
  "isNear",
  GREEN,
  isNearCallback
};

Proximity proximity;
bool isSomeoneTalking;

void setup() {
  int i;
  Serial.begin(9600);

  for (i = 0; i < nLeds; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }

  proximity = noOneNear;
  digitalWrite(proximity.led, HIGH);
  Serial.println(proximity.stateName);

  isSomeoneTalking = false;
  delay(TALK_THRESHOLD);
}

void loop() {
  int distance = sensor.convert_cm(sensor.ping_median(PINGS));
  int prevLed = proximity.led;
  bool prevTalking = isSomeoneTalking;
  
  proximity = proximity.callback(distance);
  isSomeoneTalking = talkingSensor.isTalking();

  if (prevLed != proximity.led) {
    Serial.println(proximity.stateName);
    digitalWrite(prevLed, LOW);
    digitalWrite(proximity.led, HIGH);
  }

  if (prevTalking != isSomeoneTalking && isSomeoneTalking)
    Serial.println("talking");
  else if (prevTalking != isSomeoneTalking && !isSomeoneTalking)
    Serial.println("silence");  
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

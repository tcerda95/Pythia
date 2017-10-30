#include <TalkingSensor.h>
#include <elapsedMillis.h>
#include <NewPing.h>

const int YELLOW = 9;
const int GREEN = 10;
const int RED = 11;
const int MAX_DISTANCE = 125; // in centimeters
const int NEAR_ENOUGH_MILLIS = 1500; // One and a half seconds
const int TRIGGER = 2;
const int ECHO = 3;
const int PINGS = 15;
const int TALKING_SENSOR_PIN = 4;
const int TALK_THRESHOLD = 2750;

const int FIRST_LED = 5;
const int LAST_LED = 13;

elapsedMillis someoneNearTime;
NewPing sensor(TRIGGER, ECHO, MAX_DISTANCE);
TalkingSensor talkingSensor(TALKING_SENSOR_PIN, TALK_THRESHOLD);

typedef struct proximity {
  char * stateName;
  struct proximity (*callback) (int);
} Proximity;

Proximity noOneNearCallback(int distance);
Proximity mayBeNearCallback(int distance);
Proximity isNearCallback(int distance);

const Proximity noOneNear = {
  "noOneNear",
  noOneNearCallback
};

const Proximity mayBeNear = {
  "mayBeNear",
  mayBeNearCallback
};

const Proximity isNear = {
  "isNear",
  isNearCallback
};

Proximity proximity;
bool isSomeoneTalking;

void setup() {
  int i;
  Serial.begin(9600);

  for (i = FIRST_LED; i <= LAST_LED; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }

  proximity = noOneNear;
  Serial.println(proximity.stateName);

  isSomeoneTalking = false;
  delay(TALK_THRESHOLD);
}

void loop() {
  int distance = sensor.convert_cm(sensor.ping_median(PINGS));
  char * prevState = proximity.stateName;
  bool prevTalking = isSomeoneTalking;
  
  proximity = proximity.callback(distance);
  isSomeoneTalking = talkingSensor.isTalking();

  if (Serial.available()) {
    turnOffLeds();
    turnOnSerialLeds();    
  }

  if (prevState != proximity.stateName)
    Serial.println(proximity.stateName);

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

void turnOffLeds() {
  for (int i = FIRST_LED; i <= LAST_LED; i++)
    digitalWrite(i, LOW);  
}

void turnOnSerialLeds() {
  while (Serial.available()) {
    byte led = Serial.read();
    digitalWrite(led, HIGH);
    delay(2);  // wait a bit for the rest of the bytes to become available
  }
}

boolean hasBeenNearEnough() {
  return someoneNearTime > NEAR_ENOUGH_MILLIS;
}

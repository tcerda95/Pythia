
#include <TalkingSensor.h>

const int LED = 10 ;
const int DIGITAL_PIN = 13;

TalkingSensor talkingSensor(DIGITAL_PIN);  // Build sensor with default talkingThreshold

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {
  if (talkingSensor.isTalking()) {
    digitalWrite(LED, HIGH);
    Serial.println(F("someone is talking"));
  }
  else {
    digitalWrite(LED, LOW);
    Serial.println(F("silence"));
  }
}

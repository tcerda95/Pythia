
const int T2 = A4;  // NEXT


void setup() {
  Serial.begin(9600);
  pinMode(T2, OUTPUT);
  digitalWrite(T2, LOW);
}

void loop() {
  Serial.println("LOW");
  delay(1000);
  digitalWrite(T2, HIGH);
  Serial.println("HIGH");
  delay(1000);
  digitalWrite(T2, LOW);
}

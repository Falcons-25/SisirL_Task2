const int trigPin = 9;
const int echoPin = 8;
long duration;
int distance;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // send out a pulse to calculate the duration it takes to return
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  // calculates distance based on speed of sound (appx. 1000ft/s)
  distance = duration * 1/2000;
  // prints the integer value of distance
  Serial.println(distance);
  delayMicroseconds(10000);
}
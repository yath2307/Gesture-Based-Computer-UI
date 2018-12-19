
#include <NewPing.h>

#define TRIGGER_PIN1 8

#define ECHO_PIN1 9

#define TRIGGER_PIN2 10

#define ECHO_PIN2 11

#define TRIGGER_PIN3 12

#define ECHO_PIN3 13

#define MAX_DISTANCE 200

NewPing sonar1(TRIGGER_PIN1, ECHO_PIN1, MAX_DISTANCE);
NewPing sonar2(TRIGGER_PIN2, ECHO_PIN2, MAX_DISTANCE);
NewPing sonar3(TRIGGER_PIN3, ECHO_PIN3, MAX_DISTANCE);

void setup() {

Serial.begin(9600);

}

void loop() {

unsigned int uS1 = sonar1.ping();
unsigned int uS2 = sonar2.ping();
unsigned int uS3 = sonar3.ping();

Serial.println("yes");

pinMode(ECHO_PIN1,OUTPUT);
digitalWrite(ECHO_PIN1,LOW);
pinMode(ECHO_PIN1,INPUT);
Serial.println(uS1 / US_ROUNDTRIP_CM);

pinMode(ECHO_PIN2,OUTPUT);
digitalWrite(ECHO_PIN2,LOW);
pinMode(ECHO_PIN2,INPUT);
Serial.println(uS2 / US_ROUNDTRIP_CM);

pinMode(ECHO_PIN3,OUTPUT);
digitalWrite(ECHO_PIN3,LOW);
pinMode(ECHO_PIN3,INPUT);
Serial.println(uS3 / US_ROUNDTRIP_CM);

}

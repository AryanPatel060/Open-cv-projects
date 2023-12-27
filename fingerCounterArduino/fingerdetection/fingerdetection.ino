const int numLeds = 5;  // Change this to the number of LEDs you have
int ledPins[] = {2, 3, 4, 5, 6};  // Change these pin numbers based on your wiring
String cmd;
void setup() {
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  Serial.begin(9600);
}

void loop() {
  while(Serial.available()!=0) 
  {
  
  }
 
    cmd = Serial.readStringUntil('\r');
//    cmd = "01000";
//    Serial.println(cmd);
    for (int i = 0; i < numLeds; i++) {
//      Serial.println(i);
      if (cmd.charAt(i) == '1') {
        digitalWrite(ledPins[i], HIGH);
//        
      } else {
        digitalWrite(ledPins[i], LOW);
//        Serial.println(i);
      }
    }
  
}

String cmd ; 
void setup() {
    // put our setupcode here, to run once:
  Serial.begin(9600);
 }
void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()==0) 
  {
     pinMode(13,OUTPUT);    
  }
  cmd = Serial.readStringUntil('\r');
  if(cmd == "ON")
  {
   digitalWrite(13,HIGH); 
  }
  if(cmd == "OFF")
  {
   digitalWrite(13,LOW); 
  }
}

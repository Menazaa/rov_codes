char ser;
void setup() {
  
pinMode(13,1);
Serial.begin(9600);

}

void loop() {
  if(Serial.available() > 0){
    
    ser= Serial.read();
    Serial.println(ser);
    }
  if(ser == '1'){
    digitalWrite(13,1);
    }else{
     digitalWrite(13,0);

    }


}

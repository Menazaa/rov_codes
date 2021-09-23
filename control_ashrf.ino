char m =' ';

char x[2] = "  ";

 
void setup() {
Serial.begin(9600);
for(int i=2; i<=11; i++){
  pinMode(i,1);
  }
}

void loop() {
  if(Serial.available() >0){   
    x[0] =Serial.read();
    
    while(!Serial.available() >0){}
    Serial.println("enterd");
    Serial.println(x[0]);
    Serial.println(x[1]);

    x[1] =Serial.read();
    
    if(x[0] == 'a' && x[1] == 'a'){
      analogWrite(5,50);
      }
      
    else if(x[0] == 'b' && x[1] == 'b'){
      analogWrite(5,170);
      }

    
    else if(x[0] == 'c' && x[1] == 'c'){
      analogWrite(5,255);
      }

    
    else if(x[0] == 'd' && x[1] == 'd'){
      analogWrite(3,50);
      }

    
    else if(x[0] == 'e' && x[1] == 'e'){
      analogWrite(3,170);
      }
      
    else if(x[0] == 'f' && x[1] == 'f'){
      analogWrite(3,255);
      }

    else if(x[0] == 'p' && x[1] == 'p'){
      analogWrite(9,50);
      }
      
    else if(x[0] == 'q' && x[1] == 'q'){
      analogWrite(9,170);
      }
            
    else if(x[0] == 'r' && x[1] == 'r'){
      analogWrite(9,255);
      }
      
    else if(x[0] == 's' && x[1] == 's'){
      analogWrite(10,50);
      }
      
    else if(x[0] == 't' && x[1] == 't'){
      analogWrite(10,170);
      }
            
    else if(x[0] == 'u' && x[1] == 'u'){
      analogWrite(10,255);
      }

      
      
    else if((x[0] == 'Z' && x[1] == 'r') || (x[0] == 'r' && x[1] == 'Z')){
      digitalWrite(6,1);
      }
    
    else if((x[0] == 'X' && x[1] == 'u') || (x[0] == 'u' && x[1] == 'X')){
      digitalWrite(2,1);
    }
    else if((x[0] == 'C' && x[1] == 'C') || (x[0] == 'C' && x[1] == 'C')){
      digitalWrite(11,1);
    }
    else if(x[0] == 'o' && x[1] == 'o'){
      
      analogWrite(5,0);
      analogWrite(3,0);
      analogWrite(6,0);
      analogWrite(9,0);
      analogWrite(10,0);
      digitalWrite(11,0);

      digitalWrite(2,0);

      }
 
     
  }
     
     


}

#include<Wire.h>
#include<SoftwareSerial.h>
#include<Servo.h>

#define thrust_pin1 7       //defining thrusters' pins (PWM pins)
#define thrust_pin2 8
#define thrust_pin3 9
#define thrust_pin4 10
#define thrust_pin5 11

#define action_pin1 22      //definning some digital pins for the TOGGLE action (LEDS, DCVS,...etc)
#define action_pin2 24
#define action_pin3 26
#define action_pin4 28
#define action_pin5 30
#define action_pin6 32

/*
#define interrupt_pin1 2      //definning interrupt pins they won't be connected to anything
#define interrupt_pin2 3
#define interrupt_pin3 18
#define interrupt_pin4 19       // ANYWAY WE ARE NOT USING THAT ANYMORE 
#define interrupt_pin5 20
#define interrupt_pin6 21
*/

Servo thruster1;             //creating a servo object "thruster"
Servo thruster2;             //thrusters 1 and 2 are the frontal thrusters for forward and backward movements
Servo thruster3;             //thrusters 3 and 4 are the upper thrusters for up and down movements
Servo thruster4;
Servo thruster5;             //thruster 5 is the tail thruster for lateral movements i.e: left and right 

int thruster1_signal=1500;       //the signal sent to the ESC for example (1200)and so on for the other thrusters
int thruster2_signal=1500;
int thruster3_signal=1500;
int thruster4_signal=1500;
int thruster5_signal=1500;

/*int tnew=8;
int rnew=7;

SoftwareSerial tarek(7,8);
*/
//*******************order excution
char x=' '; //will be recieved from the joystick or raspberry pi initially set to stop 
char gyro_order;
char current_order='5';   //to avoid recieving the same value twice 
char previous_order='1';
//******************
char instruction,c[8];
  int counter;
//******************auto or manual
bool AUTO=0;                               //a flage which indicate the mode ( 0 for manual mode / 1 for autonomous mode) initially manual mode is activated
//**************************
//*********************gyroscope
const int MPU_addr=0x68;
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

int minVal=265;
int maxVal=402;

double gyro_x;
double gyro_y;
double gyro_z;
//*************************

void setup() {
  Serial.begin(9600);   //115200 by ashraf
  Wire.begin();
  /*
  tarek.begin(9600);    //115200 by ashraf
  */

//**************************to test on leds***************\\
pinMode(2,OUTPUT);
pinMode(3,OUTPUT);
pinMode(4,OUTPUT);
pinMode(5,OUTPUT);





  pinMode(action_pin1,OUTPUT);                        //SETTING THE PINS (DIGITAL Output)
  pinMode(action_pin2,OUTPUT);
  pinMode(action_pin3,OUTPUT);
  pinMode(action_pin4,OUTPUT);
  pinMode(action_pin5,OUTPUT);
  pinMode(action_pin6,OUTPUT);

  
  thruster1.attach(thrust_pin1);           //attaching thrusters pins...
  thruster2.attach(thrust_pin2);
  thruster3.attach(thrust_pin3);
  thruster4.attach(thrust_pin4);
  thruster5.attach(thrust_pin5);

  thruster1.writeMicroseconds(1500);       //send "stop" signal to each ESC
  thruster2.writeMicroseconds(1500);
  thruster3.writeMicroseconds(1500);
  thruster4.writeMicroseconds(1500);
  thruster5.writeMicroseconds(1500);

  delay(1000);                             //delay till the ESC recognize the "stop" signal

  thruster1.writeMicroseconds(1550);       //check that all thrusters are working properly  
  thruster2.writeMicroseconds(1550);       //VERY LOW SPEED IS USED TO MINIMIZE CURRENT
  thruster3.writeMicroseconds(1550);
  thruster4.writeMicroseconds(1550);
  thruster5.writeMicroseconds(1550);

  delay(1000);                             // to be able to see the thrusters running initially 

  thruster1.writeMicroseconds(1500);       //send "stop" signal to each ESC
  thruster2.writeMicroseconds(1500);
  thruster3.writeMicroseconds(1500);
  thruster4.writeMicroseconds(1500);
  thruster5.writeMicroseconds(1500);
  
}

void loop() 
{

  if(AUTO==0)                                            //check which mode you are in .. this case (manual mode)
  {
    while(1)                                             // manual mode code ...
    {
        
     /* x=character_filter();
      Serial.println(x);
     */

 if(Serial.available()>0)                 //if the serial is active
  {
   current_order=Serial.read();                   //take in the value sent
   Serial.write(current_order);                    //and send that value through software serial
   if (current_order!=previous_order)                          //if the new value is not the same of the previous
    {
     previous_order=current_order;          //change the previous value
     x=current_order;
    }
  }
  switch(x)                               //start switching
  {
   
    case 'a':                                     //put the configuration which moves you forward with first speed CHECK ROV FUNCTIONS

    ROV_forward_speed1();
    analogWrite(2,80);
    analogWrite(3,0);
    analogWrite(4,0);
    analogWrite(5,0);
    break;
    
    case 'b':                                     //put the configuration which moves you forward with second speed

    ROV_forward_speed2();
    analogWrite(2,160);
    analogWrite(3,0);
    analogWrite(4,0);
    analogWrite(5,0);
    break;
    
    case 'c':                                     //put the configuration which moves you forward with third speed

    ROV_forward_speed3();
    analogWrite(2,255);
    analogWrite(3,0);
    analogWrite(4,0);
    analogWrite(5,0);
    break;
    
    case 'd':                                      //put the configuration which moves you backward with the first speed

    ROV_backward_speed1();
    analogWrite(2,0);
    analogWrite(3,80);
    analogWrite(4,0);
    analogWrite(5,0);
    break;
    
    case 'e':                                      //put the configuration which moves you backward with the second speed

    ROV_backward_speed2();
    analogWrite(2,0);
    analogWrite(3,160);
    analogWrite(4,0);
    analogWrite(5,0);
    break;
    
    case 'f':                                      //put the configuration which moves you backward with the third speed

    ROV_backward_speed3();
    analogWrite(2,0);
    analogWrite(3,255);
    analogWrite(4,0);
    analogWrite(5,0);
    break;
    
    case 'o':                                      //put the configuration which stops you
    
    ROV_stop();
    analogWrite(2,0);
    analogWrite(3,0);
    analogWrite(4,0);
    analogWrite(5,0);
    break;

    case 'i':                                      //put the configuration which moves you up with the first speed

    ROV_upward_speed1();
    
    break;

    case 'j':                                      //put the configuration which moves you up with the second speed

    ROV_upward_speed2();

    break;

    case 'k':                                      //put the configuration which moves you up with the full speed

    ROV_upward_speed3();
    
    break;

    case 'l':                                      //put the configuration which moves you down with the first speed

    ROV_downward_speed1();

    break;

    case 'm':                                      //put the configuration which moves you down with the second speed

    ROV_downward_speed2();

    break;

    case 'n':                                      //put the configuration which moves you down with the full speed

    ROV_downward_speed3();

    break;

    case 'p':                                      //put the configuration which moves you right with the first speed

    ROV_right_speed1();
    analogWrite(2,0);
    analogWrite(3,0);
    analogWrite(4,80);
    analogWrite(5,0);
    break;

    case 'q':                                      //put the configuration which moves you right with the second speed

    ROV_right_speed2();
    analogWrite(2,0);
    analogWrite(3,0);
    analogWrite(4,160);
    analogWrite(5,0);
    break;

    case 'r':                                      //put the configuration which moves you right with the full speed

    ROV_right_speed3();
    analogWrite(2,0);
    analogWrite(3,0);
    analogWrite(4,255);
    analogWrite(5,0);
    break;

    case 's':                                      //put the configuration which moves you left with the first speed

    ROV_left_speed1();
    analogWrite(2,0);
    analogWrite(3,0);
    analogWrite(4,0);
    analogWrite(5,80);
    break;

    case 't':                                      //put the configuration which moves you left with the second speed

    ROV_left_speed2();
    analogWrite(2,0);
    analogWrite(3,0);
    analogWrite(4,0);
    analogWrite(5,160);
    break;

    case 'u':                                      //put the configuration which moves you left with the full speed

 
    ROV_left_speed3();
    analogWrite(2,0);
    analogWrite(3,0);
    analogWrite(4,0);
    analogWrite(5,255);
    break;

    


    case 'x':                            //if you want to change mode send x and the flag will be changed 

    AUTO=1;

    break;

    case 'A' :                  // toggle a digital pin for LEDs and DCVs
    digitalWrite(action_pin1,!digitalRead(action_pin1));        
    
    x=' ';                       // returning the variable x to a "space" to prevent geting into this action once more
    break;
    
    case 'B' :
    digitalWrite(action_pin2,!digitalRead(action_pin2));         
    
    x=' ';
    break;
    
    case 'C' :
    digitalWrite(action_pin3,!digitalRead(action_pin3));        
    
    x=' ';
    break;
    
    case 'D' :
    digitalWrite(action_pin4,!digitalRead(action_pin4));        
    
    x=' ';
    break;
    
    case 'E' :
    digitalWrite(action_pin5,!digitalRead(action_pin5));        
    
    x=' ';
    break;
    
    case 'F' :
    digitalWrite(action_pin6,!digitalRead(action_pin6));        
    
    x=' ';
    break;


    default:
        ROV_stop();
        break;
  }
        thruster1.writeMicroseconds(thruster1_signal);          //excution on the thrusters according to the o/p of the switch case 
        thruster2.writeMicroseconds(thruster2_signal);
        thruster3.writeMicroseconds(thruster3_signal);
        thruster4.writeMicroseconds(thruster4_signal);
        thruster5.writeMicroseconds(thruster5_signal);  


          if(AUTO==1)                                       //check for every loop if the mode is changed or no and break if so
      {
        Serial.println("switched to Auto");
        break;
      }
        }
      }
  





//*********************************************Autonomous Code****************************************************\\
 else if (Auto==1)                                            //check which mode you are in .. this case (autonomous mode)
  {
    x=' ';                //resetting the excution variable
    previous_order=' ';
    while(1)                                            //autonomous mode code ...
    {
      if(Serial.available()>0)
      {
        current_order=Serial.read();
        gyro_order=gyro_order_generator();
         if(gyro_order=='v'||gyro_order=='w')
         {
          current_order=gyro_order;
         }
         if(previous_order!=current_order)
        {
          previous_order=current_order;
          x=current_order;
        }
        switch(x)
        {
          case 'v' :
//          tarek.println("tilt left");

          break;

          case 'w' :
//          tarek.println("tilt right");

          break;

           case 'a' :
 //         tarek.println("up from ip");

          break;

           case 'b' :
 //         tarek.println("down from ip");

          break;

          case 'c' :
//          tarek.println("right from ip");

          break;
          
          case 'd' :
//          tarek.println("left from ip");

          break;
        }
        
      }
      

      if(AUTO==0)                                       //check foe every loop if the mode has changed or no and breaks if so
      {
        break;
      }
    }
  }
     
  delay(1);                                       // RECOMMENDED BY MOHAMMAD ASHRAF ana maleesh da3wa ^_^ Tarek 
    }
  

  


  




//************************GYRO*******************\\

char gyro_order_generator()
{
  char order;
    Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);
  AcX=Wire.read()<<8|Wire.read();
  AcY=Wire.read()<<8|Wire.read();
  AcZ=Wire.read()<<8|Wire.read();
    int xAng = map(AcX,minVal,maxVal,-90,90);
    int yAng = map(AcY,minVal,maxVal,-90,90);
    int zAng = map(AcZ,minVal,maxVal,-90,90);

       gyro_x= RAD_TO_DEG * (atan2(-yAng, -zAng)+PI);
       gyro_y= RAD_TO_DEG * (atan2(-xAng, -zAng)+PI);
       gyro_z= RAD_TO_DEG * (atan2(-yAng, -xAng)+PI);



      
    if( (gyro_y>5) && (gyro_y<50) ){                //tilting right need to tilt left

         order='v';
      }
      
      
    else if((gyro_y>300) && (gyro_y<355)){                 //tilting left need to tilt right

         order='w';
      }
    else
    {
      order='n';                                          //that one won't be checked we check on the w and v only 
    }
      return(order);
}



//***********************************************************************************************************************\\
//***********************************************************************************************************************\\
//***********************************************************************************************************************\\



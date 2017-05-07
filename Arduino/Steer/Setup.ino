#include<SoftwareSerial.h>


SoftwareSerial piSerial (3,4);

void setup()
{
  pinMode(LED_PIN, OUTPUT); //configure LED for output
  pinMode(RELAY1_PIN, OUTPUT); //configure RELAY1 for output //Pin 5
  pinMode(RELAY2_PIN, OUTPUT); //configure RELAY2 for output //Pin 6
  pinMode(RELAY3_PIN, OUTPUT); //configure RELAY3 for output //Pin 7
  pinMode(RELAY4_PIN, OUTPUT); //configure RELAY4 for output //Pin 8
  pinMode(RELAY5_PIN, OUTPUT); //configure RELAY5 for output //Pin 9
  pinMode(RELAY6_PIN, OUTPUT); //configure RELAY6 for output //Pin 10
  pinMode(RELAY7_PIN, OUTPUT); //configure RELAY7 for output //Pin A4
  pinMode(RELAY8_PIN, OUTPUT); //configure RELAY8 for output //Pin A5
  
  pinMode(DIR_PIN, OUTPUT); //D11 PB3 direction pin of PWM Board
      
  pinMode(WORKSW_PIN, INPUT_PULLUP);   //Pin D4 PD4
    
  Serial.begin(19200);  //open serial port
  piSerial.begin(9600);
  
} 

void sendData(float distance, float delta, int velocity, float sAngle){
    piSerial.print("dist,delta,vel,sAngle: ");
    piSerial.print(distance);
    piSerial.print(" ");
    piSerial.print(delta);
    piSerial.print(" ");
    piSerial.print(velocity);
    piSerial.print(" ");
    piSerial.print(sAngle);
    piSerial.println(" ");
}




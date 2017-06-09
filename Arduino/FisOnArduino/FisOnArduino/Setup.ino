#define LED_PIN 13 
  
  #define   DIR_PIN    12  //PB4
  #define   PWM_PIN    11  //PB3
  
  #define WORKSW_PIN 4  //PD4
  
  #define RELAY1_PIN 5  //PD5
  #define RELAY2_PIN 6  //PD6
  #define RELAY3_PIN 7  //PD7
  #define RELAY4_PIN 8  //PB0
  #define RELAY5_PIN 9  //PB1
  #define RELAY6_PIN 10  //PB2
  #define RELAY7_PIN A4  //PC4
  #define RELAY8_PIN A5  //PC5
  


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
  
  
  
} 






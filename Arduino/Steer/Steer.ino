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
  
  #define RAD2GRAD 57.2957795

  byte relay = 0, workSwitch = 0, speeed = 0;
  float distanceError = 0;
  int headingError = 0;
   
  float steeringPosition = 512;
  float sAngle = 50;
 
  bool isDataFound = false, isSettingFound = false;
  int header = 0, tempHeader = 0, temp;
void loop()
{
  // header high/low, relay byte, speed byte, high distance, low distance, high delta, low delta, PID Settings byte
  if (Serial.available() > 0 && !isDataFound && !isSettingFound) //find the header, 127H + 254L = 32766
  {
    int temp = Serial.read();
    header = tempHeader << 8 | temp;               //high,low bytes to make int
    tempHeader = temp;                             //save for next time
    if (header == 32766) isDataFound = true;     //Do we have a match? 
    if (header == 32764) isSettingFound = true;     //Do we have a match? 
   }
  
  //Header has been found, presumably the next 6 bytes are the data
  if (Serial.available()> 5 && isDataFound)
  {  
    relay = Serial.read();   // read relay control from AgOpenGPS
    speeed = Serial.read()>>2;  //single byte
    distanceError = (float)(Serial.read() << 8 | Serial.read());   //high,low bytes     
    headingError = (float)(Serial.read() << 8 | Serial.read());     //high low bytes 
    
    isDataFound = false;    
    workSwitch = digitalRead(WORKSW_PIN);  // read work switch
    SetRelays();
  
    steeringPosition = (analogRead(A0));   //read the steering position sensor
    sAngle = map1(steeringPosition, 0, 1023, 0, 100);
    
    sendData(distanceError, headingError, speeed, sAngle);
    
    steeringPosition = steeringPosition - 512;
      Serial.print(steeringPosition);
      Serial.print(" ");    
      Serial.print(0);
      Serial.print(" ");    
      Serial.print(0);
      Serial.print(" ");    
      Serial.print(0);
      Serial.print(" ");    
      Serial.println(0);
    
  }
  
  //Header has been found, presumably the next 5 bytes are the settings
  if (Serial.available() > 4 && isSettingFound)
  {  
    isSettingFound = false; 
  }
   	
}

float map1(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}  




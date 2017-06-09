
  
  #define STEER_RATE 1 //steering multiplier
  #define STEER_BASE 10 //minimum PWM value for valve
  

  
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
    
   
    integrate(steeringPosition);
    
    
    // Read Input: distance
    g_fisInput[0] = distanceError;
    // Read Input: delta
    g_fisInput[1] = headingError;
    // Read Input: speed
    g_fisInput[2] = speeed;

    g_fisOutput[0] = 0;

    fis_evaluate();

    
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


int integrate(int sangle){
  int error = g_fisOutput[0] - sangle;
  
  if(error < 0){  //left steer
    //activate coil 1
    int val = error * STEER_RATE;
    val = 0 - val;
    if(val > 0 and val <= STEER_BASE){
      val = STEER_BASE;
    }
    analogWrite(1, val);
    analogWrite(2, 0);
  }
  
  if(error > 0){  //right steer
    //activate coil 1
    int val = error * STEER_RATE;
    if(val > 0 and val <= STEER_BASE){
      val = STEER_BASE;
    }
    analogWrite(1, 0);
    analogWrite(2, val);
  }
  
}

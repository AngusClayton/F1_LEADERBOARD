//setup for wemos
//lane A - a0
//lane B - D11 or arduino pin 13

void setup() {
Serial.begin(9600);
Serial.println("");

}

void loop() {
  unsigned long startTime = millis(); //declare varible
  unsigned long laneATime=0;
  unsigned long laneBTime=0;
  Serial.print("=== COUNTING... ===");
  Serial.println("");
  if (true) //PUT BUTTON HERE
  {
    startTime = millis();
    
    bool raceEnd = false;
    while(raceEnd != true) 
    {
      int laneA = analogRead(A0); int laneB = digitalRead(13);
      
      if (laneA > 1000) {laneATime = millis();}
      if (laneB == 1)   {laneBTime = millis();}

      if (laneATime != 0 && laneBTime != 0) {raceEnd = true;} //end race if times recorded for both cars
      
      unsigned long currentTime = millis()-startTime;
      if ((currentTime) > 5000) {raceEnd = true;} //end if car took too long
      
      delay(1);
    }
  }
  //see if DNF:
  if (laneATime == 0) {laneATime = 5000;}
  if (laneBTime == 0) {laneBTime = 5000;}
  //calculate times:


  
  laneATime = laneATime - startTime;
  laneBTime = laneBTime - startTime;
  //float laneATimeHR = laneATime / 10000UL;
  //float laneBTimeHR = laneBTime / 10000UL;

  
  Serial.print("===== RESULTS =====");
  Serial.println("");
  Serial.print("LANE A: "); Serial.print(laneATime);
  Serial.print(" LANE B: "); Serial.println(laneBTime);
  
  if (laneATime < laneBTime) {Serial.print("LANE A WINS!");}
  else if (laneATime > laneBTime) {Serial.print("LANE B WINS!");}
  else {Serial.print("TIE!");}
  delay(50000);
  
}

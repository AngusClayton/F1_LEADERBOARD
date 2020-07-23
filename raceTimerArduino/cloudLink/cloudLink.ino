#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
//setup for wemos
//lane A - a0
//lane B - D11 or arduino pin 13
//button d14 or ard 4
/*some stuff to note for host:
 * getData = "?timeA=" + Aweb + "&timeB=" + Bweb ;  //Note "?" added at front
 * Link = "http://webhook.site/9dbc01ad-1161-4af8-8880-addb10e7a021" + getData;
 * ALSO LINK MUST BE HTTP!!
 */


/* Set these to your network credentials. */
const char *ssid = "Clayton's";  //ENTER YOUR WIFI SETTINGS
const char *password = "Cl@yt0n$";
const char *host = "webhook.site";




void setup() {
 //setup serial
Serial.begin(115200);
Serial.println("");
//wifi setup...
WiFi.mode(WIFI_OFF);        //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA);        //This line hides the viewing of ESP as wifi hotspot
  
  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.println("");

  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  //If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP

}

void loop() {
  //declare varibles 
  unsigned long startTime = millis(); //declare varible
  unsigned long laneATime=0;
  unsigned long laneBTime=0;

  //////TIMEING CODE
  
  Serial.print("=== READY ===");
  Serial.println("");
  while (digitalRead(4)==LOW) {} //wait 4 button press
  if (1 == 1) 
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
      
      delay(1);//for accuracy
    }
  } //timeing finished


  
  //see if DNF:
  if (laneATime == 0) {laneATime = 5000;}
  if (laneBTime == 0) {laneBTime = 5000;}
  //calculate times:


  
  laneATime = laneATime - startTime;
  laneBTime = laneBTime - startTime;
  //float laneATimeHR = laneATime / 10000UL;
  //float laneBTimeHR = laneBTime / 10000UL;


  if (laneATime > 5000) {laneATime = 5000;}
  if (laneBTime > 5000) {laneBTime = 5000;}

  ///serial print results
  Serial.print("===== RESULTS =====");
  Serial.println("");
  Serial.print("LANE A: "); Serial.print(laneATime);
  Serial.print(" LANE B: "); Serial.println(laneBTime);
  
  if (laneATime < laneBTime) {Serial.print("LANE A WINS!");}
  else if (laneATime > laneBTime) {Serial.print("LANE B WINS!");}
  else {Serial.print("TIE!");}


  //WIFI CODE:

  HTTPClient http;    //Declare object of class HTTPClient

  String Aweb,Bweb, getData, Link; //declate strings
  Aweb = (String)laneATime;    //convert times to strings
  Bweb = (String)laneBTime;

  //GET Data
  getData = "?timeA=" + Aweb + "&timeB=" + Bweb;  //Note "?" added at front
  Link = "http://webhook.site/9dbc01ad-1161-4af8-8880-addb10e7a021" + getData;
  //now send dat.
  http.begin(Link);     //Specify request destination
  
  int httpCode = http.GET();            //Send the request
  String payload = http.getString();    //Get the response payload

  if (httpCode == 200) {Serial.println("SUCCESSFULL UPLOAD!");}
  else  {Serial.println("ERR UPLOADING, PLEASE MANUALLY ADD TIMES");}

  http.end();  //Close connection
  
















  
  
  //tempoary delay as there is no button. remove once button setup.
  delay(50000000);
  
}

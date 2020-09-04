#include <Arduino.h>
#include <string>
#include <EEPROM.h>

// #include <ESP8266mDNS.h>
#include <ESP8266HTTPClient.h>
// #include <ESP8266HTTPUpdateServer.h>

#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <WiFiManager.h> 
#include <FirebaseArduino.h>


ESP8266WebServer server(80); // Create a webserver object listens HTTP request on port 80

const char* Name="";
const char* passwd="";
const char* DeviceOwner="000001";
const char* DeviceType="4";
const char* Regulators="0";
const char* Registrationno="1234567890";

int count = 1;
int countx=1;
int len = 0;

// const char* ssid = "Chirag-3"; //Enter Wi-Fi SSID
// const char* password =  "chirag12357"; //Enter Wi-Fi Password

String Switch1 = "";
String Switch2 = "";
String Switch3 = "";
String Switch4 = "";
String Switch5 = "";
String Switch6 = "";
String data = "";
String Switch = "";

int Switch1_pin = 16;
int Switch2_pin = 5;
int Switch3_pin = 4;
int Switch4_pin = 0;
int Switch5_pin = 2;
int Switch6_pin = 14;


// void connectWifi(){
//   WiFi.begin(Name, passwd);  //Connect to the WiFi network

//   while (WiFi.status() != WL_CONNECTED) {  //Wait for connection
//     delay(500);
//     Serial.println("Waiting to connect...");
//   }

//   Serial.print("IP address: ");
//   Serial.println(WiFi.localIP());  //Print the local IP

// }


// void handleRoot() {                          // When URI / is requested, make login Webpage
//   server.send(200, "text/html", "<form action=\"/login\" method=\"POST\"><input type=\"text\" name=\"SSID\" placeholder=\"SSID\"></br><input type=\"password\" name=\"Password\" placeholder=\"Password\"></br><input type=\"text\" name=\"Owner-ID\" placeholder=\"Owner-ID\"></br><input type=\"submit\" value=\"Submit\"></form><p>Please enter your WiFi SSID(Name) and Password</p>");
// }

// void handleLogin() {                                                         //Handle POST Request
//   String SSID = "";
//   String Password = "";
//   String OwnerID="";
//   if ( ! server.hasArg("SSID") || ! server.hasArg("Password")
//        || server.arg("SSID") == NULL || server.arg("Password") == NULL) { // Request without data
//     server.send(400, "text/plain", "400: Invalid Request");         // Print Data on screen
//     return;
//   }
//   else {
//     SSID = server.arg("SSID");
//     Password = server.arg("Password");
//     OwnerID = server.arg("Owner-ID");
//     Name=SSID.c_str();
//     passwd=Password.c_str();
//     DeviceOwner=OwnerID.c_str();
//     server.send(200, "text/html", "<h1>Credentials recieved<h1>");
//     Serial.println(SSID);
//     Serial.println(Password);
//     Serial.println(OwnerID);
//     connectWifi();
//     WiFi.softAPdisconnect(true);
//     server.stop();
//     count++;
    
//    }
// }

// void handleNotFound() {
//   server.send(404, "text/plain", "404: Not found"); // Send HTTP status 404 (Not Found)
// }

void registerdevice(){
  Firebase.begin("logiswitch-2020.firebaseio.com","NzIGZftnkTtbBDlBatXjActNwOBWBftLLTg6hO2P");
  
  Serial.println("Connected to firebase");

  Firebase.set("/DeviceData/1234567890","");
  Firebase.set("/DeviceData/1234567890/DeviceID",Registrationno);
  Firebase.set("/DeviceData/1234567890/DeviceOwner",DeviceOwner);
  Firebase.set("/DeviceData/1234567890/DeviceType",DeviceType);
  Firebase.set("/DeviceData/1234567890/Passwd",WiFi.psk().c_str());
  Firebase.set("/DeviceData/1234567890/Regulators",Regulators);
  Firebase.set("/DeviceData/1234567890/SSID",WiFi.SSID().c_str());  
  Firebase.set("/OutputStream/1234567890","1-0/2-0/3-0/4-0");

  Firebase.get("/DeviceData/1234567890/DeviceID");
  
  Serial.println("Device registered");

  Firebase.stream("/OutputStream/1234567899");
}

void setup(){
  Serial.begin(115200); //Begin Serial at 115200 Baud
  
  // if(WiFi.status() != WL_CONNECTED){
  //   WiFi.softAP(ssid, password);
  //   IPAddress IP = WiFi.softAPIP();
  //   Serial.println(IP);
  //   server.on("/", HTTP_GET, handleRoot);         // Call 'handleRoot' function
  //   server.on("/login", HTTP_POST, handleLogin); // Call 'handleLogin' function when a POST request made to "/login"
  //   server.onNotFound(handleNotFound);           // call function "handleNotFound" when unknown URI requested
  //   server.begin();                         // start the server
  //   Serial.println("Done");
  // }
  WiFiManager WiFiManager;
  Serial.println(WiFiManager.autoConnect("LogiSwitch","united_intelligence"));
  delay(5000);

  if(WiFi.status() == WL_CONNECTED ){
      Serial.println("connected...yeey :)");
      Serial.println(WiFi.SSID());
      Serial.println(WiFi.psk());
      registerdevice();
      count++;
  }
  
  pinMode(Switch1_pin,OUTPUT);
  pinMode(Switch2_pin,OUTPUT);
  pinMode(Switch3_pin,OUTPUT);
  pinMode(Switch4_pin,OUTPUT);
  pinMode(Switch5_pin,OUTPUT);
  pinMode(Switch6_pin,OUTPUT);
  digitalWrite(Switch1_pin,HIGH);
  digitalWrite(Switch2_pin,HIGH);
  digitalWrite(Switch3_pin,HIGH);
  digitalWrite(Switch4_pin,HIGH);
  digitalWrite(Switch5_pin,HIGH);
  digitalWrite(Switch6_pin,HIGH);
}

void proccess_data(String Switch){
  String Switch_number = Switch.substring(0,1);
  String Switch_state = Switch.substring(2,3);
  Serial.println(Switch_number);
  Serial.println(Switch_state);
  if(Switch_number=="1"){
    if(Switch_state=="1"){
      digitalWrite(Switch1_pin,LOW); //ON
      Serial.println("Switch 1 - ON");
    }
    else{
      digitalWrite(Switch1_pin,HIGH); //OFF
      Serial.println("Switch 1 - OFF");
    }
  }
  else if(Switch_number=="2"){
    if(Switch_state=="1"){
      digitalWrite(Switch2_pin,LOW);
      Serial.println("Switch 2 - ON");
    }
    else{
      digitalWrite(Switch2_pin,HIGH);
      Serial.println("Switch 2 - OFF");
    }
  }
  else if(Switch_number=="3"){
    if(Switch_state=="1"){
      digitalWrite(Switch3_pin,LOW);
      Serial.println("Switch 3 - ON");
    }
    else{
      digitalWrite(Switch3_pin,HIGH);
      Serial.println("Switch 3 - OFF");
    }
  }
  else if(Switch_number=="4"){
    if(Switch_state=="1"){
      digitalWrite(Switch4_pin,LOW);
      Serial.println("Switch 4 - ON");
    }
    else{
      digitalWrite(Switch4_pin,HIGH);
      Serial.println("Switch 4 - OFF");
    }
  }
  else if(Switch_number=="5"){
    if(Switch_state=="1"){
      digitalWrite(Switch5_pin,LOW);
      Serial.println("Switch 5 - ON");
    }
    else{
      digitalWrite(Switch5_pin,HIGH);
      Serial.println("Switch 5 - OFF");
    }
  }
  else if(Switch_number=="6"){
    if(Switch_state=="1"){  
      digitalWrite(Switch6_pin,LOW);
      Serial.println("Switch 6 - ON");
    }
    else{
      digitalWrite(Switch6_pin,HIGH);
      Serial.println("Switch 6 - OFF");     
    }
  }
}


void firebasestart(){
  if (Firebase.failed()) {
    Serial.println("streaming error");
    Serial.println(Firebase.error());
    Firebase.begin("logiswitch-2020.firebaseio.com","NzIGZftnkTtbBDlBatXjActNwOBWBftLLTg6hO2P");
    Firebase.stream("/OutputStream/1234567890");
  }
  
  if (Firebase.available()) {
    if (countx==1){
      FirebaseObject event = Firebase.readEvent();
      data = event.getString("data");
      countx++;
      Serial.println("Ready for Data receptance");
    }
    else{
      FirebaseObject event = Firebase.readEvent();
      String eventType = event.getString("type");
      eventType.toLowerCase();
      
      if (eventType == "put") {
        String path = event.getString("path");
        String data = event.getString("data");
        len=data.length();
        if (len==3){              // 1-1
          proccess_data(data);
        }
        else if(len==7){          // 1-1/2-1
          for(int i=0;i<5;i+=4){
            proccess_data(data.substring(i,i+3));
          }
        }
        else if(len==11){       // 1-1/2-1/3-1
          for(int i=0;i<9;i+=4){
            proccess_data(data.substring(i,i+3));
          }
        }
        else if(len==15){     // 1-1/2-1/3-1/4-1
          for(int i=0;i<13;i+=4){
            proccess_data(data.substring(i,i+3));
          }
        }
        else if(len==19){     // 1-1/2-1/3-1/4-1/5-1
          for(int i=0;i<17;i+=4){
            proccess_data(data.substring(i,i+3));
          }
        }
        else if(len==23){     // 1-1/2-1/3-1/4-1/5-1/6-1
          for(int i=0;i<21;i+=4){
            proccess_data(data.substring(i,i+3));
          }
        }
      }
    }
  }
}

void loop() {
  if(count==2){
    firebasestart();
  }
}
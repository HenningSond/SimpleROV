/*
Row arduino code
Rev: 3
Date 26.11.2022


----------------------------------------------verson 3
This version does not send temp and presure values, it just resend the reseaved values.
The trust vektor function is not uppdated. the one that is used now it wrong
----------------------------------------------
*/
#include <Servo.h>
//----------------------------------------------
Servo Th1;
Servo Th2;
Servo Th3;
Servo Camx;
Servo Camy;
Servo Lights;
//----------------------------------------------
float Lightus;

unsigned long LastTime = 0;
int degx = 90;
int degy = 90;
const byte numChars = 32;
char receivedChars[numChars];
String mystr = "";
boolean newData = false;
float  DataFloat[7]; // This must be larger than the incomming data array!
//----------------------------------------------
void setup() {
  Serial.begin(115200);
    
  Th1.attach(11);
  Th2.attach(10);
  Th3.attach(9);

  Th1.writeMicroseconds(1500); // send "stop" signal to ESC. Also necessary to arm the ESC.
  Th2.writeMicroseconds(1500);
  Th3.writeMicroseconds(1500);

  Camx.attach(6);
  Camy.attach(5);
  Camx.write(degx);
  Camy.write(degy);
    
  Lights.attach(3);
  Lights.writeMicroseconds(1100);
    
  delay(7000); // delay to allow the ESC to recognize the stopped signal.
}
//---------------------------------------------- Main loop
void loop() {
  //checkTime(1);

  recvWithStartEndMarkers();

  //checkTime(2);

  showNewData(); 

  //checkTime(3);

  WriteTh(DataFloat[1], DataFloat[0], DataFloat[2]);

  //checkTime(4);

  WrtieCam(DataFloat[3],DataFloat[4], 70);

  //checkTime(5);

  WriteLight(DataFloat[5]);

  //checkTime(6);

  Camx.write(degx);  
  Camy.write(degy);
   
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void decode3(){
  //test : <e2f3g4h1i1j1k>
  bool DataClean = true;
  String Datastr =  receivedChars;
  int DataStartNR[32];
  String DataTap[7];
		
	DataStartNR[0] = Datastr.indexOf("e");
	DataStartNR[1] = Datastr.indexOf("f");
	DataStartNR[2] = Datastr.indexOf("g");
	DataStartNR[3] = Datastr.indexOf("h");
	DataStartNR[4] = Datastr.indexOf("i");
  DataStartNR[5] = Datastr.indexOf("j");
  DataStartNR[6] = Datastr.indexOf("k");
    
//---------------------------------------------- checs that the message contains every index, if an character is missing the index of that character is -1
  for (int i = 0; i <= 6; i++){
      if  (DataStartNR[i] < 0){
        DataClean = false;
        break;
      }
    }
//---------------------------------------------- convert the sting to an array of floatingpoint values
  if (DataClean){
    for (int i = 0; i <= 6; i++){
      DataFloat[i]   = Datastr.substring(DataStartNR[i]+1, DataStartNR[i+1]).toFloat(); 
    }
  }	
}
//---------------------------------------------- Function that decodes the data and send data.
void showNewData() {
  if (newData == true) {
    //---------------------------------------------- decode version 3
    decode3();   
    //---------------------------------------------- send data to PI
    Serial.print(Lightus);
    Serial.print(' ');
    Serial.print(DataFloat[1]);
    Serial.print(' ');
    Serial.print(DataFloat[3]);
    Serial.print(' ');  
    Serial.print(DataFloat[4]);
    Serial.print(' ');  
    Serial.print(degx);
    Serial.print(' ');
    Serial.println(degy);  
    newData = false;
  }
}
//----------------------------------------------tha origional map() function just rewritten to work with floatingpoint
long mapSefle(float x, float in_min, float in_max, float out_min, float out_max) {
  return constrain(((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min),out_min,out_max);
}

//---------------------------------------------- Thrust vektor controll
void WriteTh(float x, float y, float z){
  float x_T = x*0.3*100;
  float y_T3 = y*0.15*100;
  float y_T2 = 2*sqrt(3)*(-y_T3);
  float y_T1 = (2/3)*y_T3;
  float z_T = z*0.1*100;

  float T1 =  x_T  + y_T1 + z_T;
  float T2 = -x_T  + y_T2 + z_T;
  float T3 =  y_T3 + z_T;
  
  float pwmT1 = mapSefle(T1, -100, 100, 1100, 1900);
  float pwmT2 = mapSefle(T2, -100, 100, 1100, 1900);
  float pwmT3 = mapSefle(T3, -100, 100, 1100, 1900);
  Th1.writeMicroseconds(pwmT1);
  Th2.writeMicroseconds(pwmT2);
  Th3.writeMicroseconds(pwmT3);

}
//---------------------------------------------- Camera controller
void WrtieCam(int x, int y, int speed){
  if (millis() >= (LastTime + speed)){
  
    degx += (-1)*x;
    degy += (1)*y;
    
    degx = constrain(degx, 60, 120);
    degy = constrain(degy, 60, 120);
    /*
    Camx.write(degx);
    Camy.write(degy);
    */
    LastTime = millis();
    
  }
}
//---------------------------------------------- Light controller
void WriteLight(float pow){
  Lightus = mapSefle(pow, -1,1 , 1100,1900);
  Lights.writeMicroseconds(Lightus);

}
//---------------------------------------------- Timer to check time between prosseses
/*
void checkTime(int no){
  Serial.print(no);
  Serial.print("  ");
  Serial.println(millis());
}
*/
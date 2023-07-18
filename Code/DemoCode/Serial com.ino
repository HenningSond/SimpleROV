
const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false;
float  DataFloat[4];
void setup() {
    Serial.begin(115200);
    Serial.println("<Arduino is ready>");
}

void loop() {
  
    recvWithStartEndMarkers(); 
    //--------------------------------------------------------Uppdates and checs the data
    if (newData == true) {
        Serial.print("This just in ... ");
        Serial.println(receivedChars);
        decode();
        newData = false;
    }
    //-------------------------------------------------------------------------------
    Serial.print(" ");
    Serial.print(DataFloat[0]);
    Serial.print(" ");
    Serial.print(DataFloat[1]);
    Serial.print(" ");
    Serial.print(DataFloat[2]);
    Serial.print(" ");  
    Serial.print(DataFloat[3]);
    Serial.print(" ");
    Serial.println("Done");
    
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

void decode(){
	//test : "<e2f3g4h5i> Valid string
	bool DataClean = true;
    String Datastr =  receivedChars;
  int DataStartNR[25];
	//------------------------------------------------- Set data markers
	DataStartNR[0] = Datastr.indexOf("e");
	DataStartNR[1] = Datastr.indexOf("f");
	DataStartNR[2] = Datastr.indexOf("g");
	DataStartNR[3] = Datastr.indexOf("h");
	DataStartNR[4] = Datastr.indexOf("i");

	//------------------------------------------------- check that all the elements are in the list
    for (int i = 0; i < 4; i++){
		//Serial.println(DataStartNR[i]); 
		if  (DataStartNR[i] < 0){
			//Serial.println("shit happend");
			DataClean = false;
			break;
		}
     }
	//------------------------------------------------- Store the data in float
    if (DataClean){
		for (int i = 0; i < 4; i++){
			DataFloat[i]   = Datastr.substring(DataStartNR[i]+1, DataStartNR[i+1]).toFloat(); 
		}
    }
}



  void resetEsp() {
  esp.println("AT+RST");
  delay(1000);
  if(esp.find("OK") ) { 
    Serial.println("Connected with IP Address");
    connectionStatus = 1;
  }
  else {
    Serial.println("Not connected, sending connection command...");
    connectionStatus = 0;
    connectWifi();
  }
}

void connectWifi() {
  esp.println("AT+CWJAP=\"Tatooine\",\"Abby0u812\"");
  
  delay(4000);
  if(esp.find("OK")) {
    Serial.println("Connected!");
  }
  else {
    Serial.println("Cannot connect to wifi."); 
  }
}

void reportReadings(float reportedYaw, float reportedPitch, float reportedRoll) {
  
   char packet[166];
   char str_reportedYaw[8];
   dtostrf(reportedYaw, 5, 1, str_reportedYaw);
   char str_reportedPitch[8];
   dtostrf(reportedPitch, 5, 1, str_reportedPitch);
   char str_reportedRoll[8];
   dtostrf(reportedRoll, 5, 1, str_reportedRoll);
   char str_yawSetPoint[8];
   dtostrf(yawSetPoint, 5, 1, str_yawSetPoint);
   char str_pitchSetPoint[8];
   dtostrf(pitchSetPoint, 5, 1, str_pitchSetPoint);
   char str_rollSetPoint[8];
   dtostrf(rollSetPoint, 5, 1, str_rollSetPoint);
/*
   String str_reportedYaw = String(reportedYaw);
   String str_reportedPitch = String(reportedPitch);
   String str_reportedRoll = String(reportedRoll);
   String str_yawSetPoint = String(yawSetPoint);
   String str_pitchSetPoint = String(pitchSetPoint);
   String str_rollSetPoint = String(rollSetPoint);*/
   
  sprintf(packet, "{ \"deviceID\":\"ac423eb65d4a32\",\"metricTypeID\":6,\"uomID\":4,\"actual\":{\"y\":%s,\"p\":%s,\"r\":%s},\"setPoints\":{\"y\":%s,\"p\":%s,\"r\":%s}}", str_reportedYaw, str_reportedPitch, str_reportedRoll, str_yawSetPoint, str_pitchSetPoint, str_rollSetPoint);
  //String packet = "{ \"readingID\":\"" + String(readingID) + "\",\"deviceID\":\"ac423eb65d4a32\",\"metricTypeID\":6,\"uomID\":4, actual\":{\"y\":" + str_reportedYaw + ",\"p\":" + str_reportedPitch + ",\"r\":" + str_reportedRoll + "},setPoints\":{\"y\":" + str_yawSetPoint + ",\"p\":" + str_pitchSetPoint + ",\"r\":" + str_rollSetPoint + "}}";
  
  int packetLength = strlen(packet);
  Serial.println(packet);
  char postRequest[137];
  
  sprintf(postRequest, "POST /LumbarSensorReading HTTP/1.1\r\nHost: 192.168.0.100\r\nAccept: */*\r\nContent-Type: application/json\r\nContent-Length: %d\r\n\r\n", packetLength);
  
  int postRequestLength = strlen(postRequest);
  
  int combinedRequestLength = postRequestLength + packetLength;
  Serial.println(postRequest);
  
  // Start the connection to the server
  esp.println("AT+CIPSTART=\"TCP\",\"192.168.0.100\",5000");//start a TCP connection.
  delayMicroseconds(500);

  // If connection OK send the packet
  if(esp.find("CONNECT")) {
    Serial.println(combinedRequestLength);

    
    //Serial.println("Packet: " + packet);
    esp.print("AT+CIPSEND=");
    esp.println(combinedRequestLength);

    // Give time for response
    delay(500);
      if(esp.find(">")) { 
        Serial.println("Sending.."); 
        esp.print(postRequest);
        esp.print(packet);
        if( esp.find("SEND OK")) { 
            Serial.println("Packet sent OK");
            /*while (esp.available()) {
              String tmpResp = esp.readString();
              Serial.println(tmpResp);
            }*/
          }
      }
  }
  else {
    Serial.println("TCP Connection NOT OK"); 
  }
  
  memset(packet, 0, sizeof(packet));
  memset(postRequest, 0, sizeof(postRequest)); 
}

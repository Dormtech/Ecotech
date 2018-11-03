//*****************************************
// @file main.ino
//@authors Ben Bellerose & Jake Smiley
//@date June 2018
//@modified November 3 2018
//modified by BB
//@brief sensor control and output through serial communication
//*****************************************

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include "HX711.h"

// Pins
int F1pin = 3; //Fire pin
int TH1pin = 8; //Temp humid pin
int WL1pin = 2; //Water level pin
int C1pin = 11; //CO2 pin
int DOUT = 4; //Weight scale
int CLK = 5; //Weight scale
int PH1pin = A7; //PH pin

//Global variables
float calibration_factor = -96650; //-106600 worked for 40Kg max scale setup
int weight_tare = 0; //Tare value for scale

//Gather Temp Humid data from sensor
byte getTHData (int pin) {
  byte data;
  for (int i = 0; i < 8; i ++) {
    if (digitalRead (pin) == LOW) {
      while (digitalRead (pin) == LOW); // wait for 50us
        delayMicroseconds (30); // determine the duration of the high level to determine the data is '0 'or '1'
      if (digitalRead (pin) == HIGH)
        data |= (1 << (7-i)); // high front and low in the post
      while (digitalRead (pin) == HIGH); // data '1 ', wait for the next one receiver
     }
  }
  return data;
}

//Read temp and humidity
void readTH (int pin) {
  int datLen = 4;
  byte dat [datLen];
  digitalWrite (pin, LOW); // bus down, send start signal
  delay (30); // delay greater than 18ms, so DHT11 start signal can be detected

  pinMode (pin, OUTPUT);
  digitalWrite (pin, HIGH);
  delayMicroseconds (40); // Wait for DHT11 response

  pinMode (pin, INPUT);
  while (digitalRead (pin) == HIGH){
    delayMicroseconds (80); // DHT11 response, pulled the bus 80us
  }
  if (digitalRead (pin) == LOW){
    delayMicroseconds (80); // DHT11 80us after the bus pulled to start sending data
  }

  for (int i = 0; i < datLen; i ++) {// receive temperature and humidity data, the polarity bit is not considered
    dat[i] = getTHData (pin);
  }

  Serial.print ("H" & str(pin) & "=");
  Serial.print (dat [0], DEC);
  Serial.print ('.');
  Serial.print (dat [1], DEC);
  Serial.print ('%');
  Serial.print(",");
  Serial.print ("T" & str(pin) & "=");
  Serial.print (dat [2], DEC);
  Serial.print ('.');
  Serial.print (dat [3], DEC);
  Serial.print('C');
  Serial.print(",");
}

//Read water level
void readWL (pin){
  pinMode(pin, INPUT);

  int WL = analogRead(pin);

  Serial.print("WL" & str(pin) & "=");
  Serial.print(WL, DEC);
  Serial.print("");
  Serial.print(",");
}

//Read fire levels
void readF(pin){
  pinMode(pin, INPUT);

  int fire = analogRead(pin);

  Serial.print("F" & str(pin) & "=");
  Serial.print(fire, DEC);
  Serial.print("");
  Serial.print(",");
}

//Read CO2 levels
void readCO2(pin){
  pinMode(pin , INPUT);

  int Th = pulseIn(pin,HIGH); //Temp HIGH
  int Tl = pulseIn(pin,LOW); //Temp LOW

  int CO2 = (2000 * (Th - 0.002)) / (Th + Tl - 0.004);

  Serial.print("C" & str(pin) & "= ");
  Serial.print(CO2, DEC);
  Serial.print(",");
}

//Read PH levels
void readPH(pin){
  pinMode(pin , INPUT);

  int measure = analogRead(pin);
  double voltage = 5 / 1024.0 * measure; //digital to voltage conversion
  float Po = 7 + ((2.5 - voltage) / 0.18);

  Serial.print("PH" & str(pin) & "= ");
  Serial.print(Po, DEC);
  Serial.print(",");
}

Adafruit_BMP280 bmp; //Pressure sensor
HX711 scale(DOUT, CLK); //Weight sensor

//////////////////
void setup() {
  Serial.begin(9600);
  scale.set_scale(-96650);
}

void loop() {
  //Read Temp Humid Values
  readTH (TH1pin);

  //Read Water Level
  readWL(WL1pin);

  //Read Fire Level
  readF(F1pin);

  //Read CO2 level
  readCO2(C1pin);

  //Read Weight
  Serial.print("W" & DOUT & "= ");
  Serial.print(scale.get_units(), DEC);
  Serial.print(" kg");
  Serial.print(",");

  //Read PH
  readPH(PH1pin);

  //Read pressure sensor
  if (!bmp.begin()) {
    Serial.print(F("T2 = NA,P1 = NA,A1 = NA"));
    while (1);
  }

  Serial.print("T75= ");
  Serial.print(bmp.readTemperature(),DEC);
  Serial.print("C");
  Serial.print(",");

  Serial.print("P75= ");
  Serial.print(bmp.readPressure(),DEC);
  Serial.print("Pa");
  Serial.print(",");

  Serial.print("A75= ");
  Serial.print(bmp.readAltitude(1013.25),DEC);
  Serial.print("m");

  Serial.println();
  delay(2000);
}

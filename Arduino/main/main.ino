//*****************************************
// @file main.ino
//@authors Ben Bellerose & Jake Smiley
//@date June 2018
//@modified June 22 2018
//modified by BB
//@brief sensor control and output through serial communication
//*****************************************

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include "HX711.h"

Adafruit_BMP280 bmp; // I2C

// Pins
int F1pin = 3;
int DH1pin = 8;
int WL1pin = 2;
int C1pin = 11;
int DOUT = 4;
int CLK = 5;
int ph_pin = A7;

HX711 scale(DOUT, CLK);


//Variables
byte dat [5];
float calibration_factor = -96650; //-106600 worked for my 40Kg max scale setup
int weight_tare = 0;

//Read Temp Humid data from sensor
byte read_data (int pin) {
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

//Test temp and humidity
void start_test (int pin) {
  digitalWrite (pin, LOW); // bus down, send start signal
  delay (30); // delay greater than 18ms, so DHT11 start signal can be detected
 
  digitalWrite (pin, HIGH);
  delayMicroseconds (40); // Wait for DHT11 response
 
  pinMode (pin, INPUT);
  while (digitalRead (pin) == HIGH);
    delayMicroseconds (80); // DHT11 response, pulled the bus 80us
  if (digitalRead (pin) == LOW);
    delayMicroseconds (80); // DHT11 80us after the bus pulled to start sending data
 
  for (int i = 0; i < 4; i ++) // receive temperature and humidity data, the polarity bit is not considered
    dat[i] = read_data (pin);
 
  pinMode (pin, OUTPUT);
  digitalWrite (pin, HIGH); // send data once after releasing the bus, wait for the host to open the next Start signal
}

//////////////////
void setup() {
  pinMode(C1pin , INPUT);
  pinMode(WL1pin, INPUT);
  pinMode (DH1pin, OUTPUT);
  pinMode(F1pin, INPUT);
  Serial.begin(9600);
  scale.set_scale(-96650);
}

void loop() {
  //Read Temp Humid Values
  start_test (DH1pin);
  Serial.print ("H1=");
  Serial.print (dat [0], DEC);
  Serial.print ('.');
  Serial.print (dat [1], DEC);
  Serial.print ('%');
  Serial.print(",");
  Serial.print ("T1=");
  Serial.print (dat [2], DEC);
  Serial.print ('.');
  Serial.print (dat [3], DEC);
  Serial.print('C');
  Serial.print(",");

  //Read Water Level
  int WL1 = analogRead(WL1pin);
  Serial.print("WL1=");
  Serial.print(WL1, DEC);
  Serial.print("");
  Serial.print(",");

  //Read Fire Level
  int F1 = analogRead(F1pin);
  Serial.print("F1=");
  Serial.print(F1, DEC);
  Serial.print("");
  Serial.print(",");

  //Read CO2 level
  int Th = pulseIn(C1pin,HIGH);
  int Tl = pulseIn(C1pin,LOW);
  int CO2;
  CO2 = (2000 * (Th - 0.002)) / (Th+Tl - 0.004);
  Serial.print("C1 = ");
  Serial.print(CO2, DEC);
  Serial.print(",");

  //Read Weight
  Serial.print("W1 = ");
  Serial.print(scale.get_units(), DEC);
  Serial.print(" kg");
  Serial.print(",");

  //Read PH
  int measure = analogRead(ph_pin);
  Serial.print("phM1 = ");
  Serial.print(measure, DEC);
  Serial.print(",");

  double voltage = 5 / 1024.0 * measure; //digital to voltage conversion
  Serial.print("V1 = ");
  Serial.print(voltage, DEC);
  Serial.print(",");
  
  float Po = 7 + ((2.5 - voltage) / 0.18);
  Serial.print("PH1 = ");
  Serial.print(Po, DEC);
  Serial.print(",");

  //Read pressure sensor
  if (!bmp.begin()) {  
    Serial.print(F("T2 = NA,P1 = NA,A1 = NA"));
    while (1);
  }

  Serial.print("T2 = ");
  Serial.print(bmp.readTemperature(),DEC);
  Serial.print("C");
  Serial.print(",");
    
  Serial.print("P1 = ");
  Serial.print(bmp.readPressure(),DEC);
  Serial.print("Pa");
  Serial.print(",");

  Serial.print("A1 = ");
  Serial.print(bmp.readAltitude(1013.25),DEC);
  Serial.print("m");
    
  Serial.println();
  delay(2000);
}

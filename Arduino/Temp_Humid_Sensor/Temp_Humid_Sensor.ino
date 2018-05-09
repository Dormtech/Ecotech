//KY015 DHT11 Temperature and humidity sensor 
int DH1pin = 8;
byte dat [5];
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
 
void setup () {
  Serial.begin (9600);
  pinMode (DH1pin, OUTPUT);
}
 
void loop () {
  start_test (DH1pin);
  Serial.print ("H1=");
  Serial.print (dat [0], DEC); // display the humidity-bit integer;
  Serial.print ('.');
  Serial.print (dat [1], DEC); // display the humidity decimal places;
  Serial.println ('%');
  Serial.print ("T1=");
  Serial.print (dat [2], DEC); // display the temperature of integer bits;
  Serial.print ('.');
  Serial.print (dat [3], DEC); // display the temperature of decimal places;
  Serial.println ('C');
  delay (7000);
}

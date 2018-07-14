String hold = "";
byte ch = 0;
void setup() {
  Serial.begin (9600);
}

void loop() {
  if (Serial.available()) 
  {
  ch = Serial.read();
  hold = String(ch);
  if (hold == "1"){ 
    int b1 = random(0,254);
    Serial.print("B1=");
    Serial.print(b1,DEC);
    Serial.print(",");
   
    int c1 = random(0,15);
    Serial.print("C1=");
    Serial.print(c1,DEC);
    Serial.print(",");
   
    int ph1 = random(0,254);
    Serial.print("PH1=");
    Serial.print(ph1,DEC);
    Serial.print(",");
   
    int t1 = random(0,40);
    Serial.print("T1=");
    Serial.print(t1,DEC);
    Serial.print("C");
    Serial.print(",");
    int t2 = random(0,40);
    Serial.print("T2=");
    Serial.print(t2,DEC);
    Serial.print("C");
    Serial.print(",");
    int t3 = random(0,40);
    Serial.print("T3=");
    Serial.print(t3,DEC);
    Serial.print("C");
    Serial.print(",");
    int t4 = random(0,40);
    Serial.print("T4=");
    Serial.print(t4,DEC);
    Serial.print("C");
    Serial.print(",");
    int t5 = random(0,254);
    Serial.print("T5=");
    Serial.print(t5,DEC);
    Serial.print("C");
    Serial.print(",");
    int t6 = random(0,40);
    Serial.print("T6=");
    Serial.print(t6,DEC);
    Serial.print("C");
    Serial.print(",");
   
    int h1 = random(0,80);
    Serial.print("H1=");
    Serial.print(h1,DEC);
    Serial.print ('%');
    Serial.print(",");
    int h2 = random(0,80);
    Serial.print("H2=");
    Serial.print(h2,DEC);
    Serial.print ('%');
    Serial.print(",");
    int h3 = random(0,80);
    Serial.print("H3=");
    Serial.print(h3,DEC);
    Serial.print ('%');
    Serial.print(",");
    int h4 = random(0,80);
    Serial.print("H4=");
    Serial.print(h4,DEC);
    Serial.print ('%');
    Serial.print(",");
    int h5 = random(0,80);
    Serial.print("H5=");
    Serial.print(h5,DEC);
    Serial.print ('%');
    Serial.print(",");
    int h6 = random(0,254);
    Serial.print("H6=");
    Serial.print(h6,DEC);
    Serial.print ('%');
    Serial.print(",");
    delay(100);
  } else if (hold == "2") {
     int w1 = random(0,254);
    Serial.print("W1=");
    Serial.print(w1,DEC);
    Serial.print(",");
    int w2 = random(0,254);
    Serial.print("W2=");
    Serial.print(w2,DEC);
    Serial.print(",");
    int w3 = random(0,254);
    Serial.print("W3=");
    Serial.print(w3,DEC);
    Serial.print(",");
    int w4 = random(0,254);
    Serial.print("W4=");
    Serial.print(w4,DEC);
    Serial.print(",");
    int w5 = random(0,254);
    Serial.print("W5=");
    Serial.print(w5,DEC);
    Serial.print(",");
    int w6 = random(0,254);
    Serial.print("W6=");
    Serial.print(w6,DEC);
    Serial.print(",");
    int w7 = random(0,254);
    Serial.print("W7=");
    Serial.print(w7,DEC);
    Serial.print(",");
    int w8 = random(0,254);
    Serial.print("W8=");
    Serial.print(w8,DEC);
    Serial.print(",");
    int w9 = random(0,254);
    Serial.print("W9=");
    Serial.print(w9,DEC);
    Serial.print(",");
    int w10 = random(0,254);
    Serial.print("W10=");
    Serial.print(w10,DEC);
    Serial.print(",");
    int w11 = random(0,254);
    Serial.print("W11=");
    Serial.print(w11,DEC);
    Serial.print(",");
    delay(100);
  }else if (hold == "3") {
    int f1 = random(0,10);
    Serial.print("F1=");
    Serial.print(f1,DEC);
    Serial.print(",");
    int f2 = random(0,10);
    Serial.print("F2=");
    Serial.print(f2,DEC);
    Serial.print(",");
    int f3 = random(0,10);
    Serial.print("F3=");
    Serial.print(f3,DEC);
    Serial.print(",");
    int f4 = random(0,10);
    Serial.print("F4=");
    Serial.print(f4,DEC);
    Serial.print(",");
    int f5 = random(0,10);
    Serial.print("F5=");
    Serial.print(f5,DEC);
    Serial.print(",");
    int f6 = random(0,10);
    Serial.print("F6=");
    Serial.println(f6,DEC);
    int b1 = random(0,254);
    Serial.print("B1=");
    Serial.print(b1,DEC);
    Serial.print(",");
    delay(100);  
  }
}
}


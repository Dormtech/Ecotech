String hold = "";
byte ch = 0;
void setup() {
  Serial.begin (9600);
}

void loop() {
   if (Serial.available()) {
    ch = Serial.read();
    hold = String(ch,HEX);
    if (hold == "31"){ 
      int c1 = random(0,15);
      Serial.write("C1=");
      Serial.write(c1);
      Serial.write(",");
     
      int t1 = random(0,40);
      Serial.write("T1=");
      Serial.write(t1);
      Serial.write("C");
      Serial.write(",");
      int t2 = random(0,40);
      Serial.write("T2=");
      Serial.write(t2);
      Serial.write("C");
      Serial.write(",");
      int t3 = random(0,40);
      Serial.write("T3=");
      Serial.write(t3);
      Serial.write("C");
      Serial.write(",");
      int t4 = random(0,40);
      Serial.write("T4=");
      Serial.write(t4);
      Serial.write("C");
      Serial.write(",");
      int t5 = random(0,254);
      Serial.write("T5=");
      Serial.write(t5);
      Serial.write("C");
      Serial.write(",");
      int t6 = random(0,40);
      Serial.write("T6=");
      Serial.write(t6);
      Serial.write("C");
      Serial.write(",");
     
      int h1 = random(0,80);
      Serial.write("H1=");
      Serial.write(h1);
      Serial.write ('%');
      Serial.write(",");
      int h2 = random(0,80);
      Serial.write("H2=");
      Serial.write(h2);
      Serial.write ('%');
      Serial.write(",");
      int h3 = random(0,80);
      Serial.write("H3=");
      Serial.write(h3);
      Serial.write ('%');
      Serial.write(",");
      int h4 = random(0,80);
      Serial.write("H4=");
      Serial.write(h4);
      Serial.write ('%');
      Serial.write(",");
      int h5 = random(0,80);
      Serial.write("H5=");
      Serial.write(h5);
      Serial.write ('%');
      Serial.write(",");
      int h6 = random(0,254);
      Serial.write("H6=");
      Serial.write(h6);
      Serial.write('%');
      Serial.write('\n');
      delay(100);
      
    } else if (hold == "32") {
       int ph1 = random(0,254);
      Serial.write("PH1=");
      Serial.write(ph1);
      Serial.write(",");
      int w1 = random(0,254);
      Serial.write("W1=");
      Serial.write(w1);
      Serial.write(",");
      int w2 = random(0,254);
      Serial.write("W2=");
      Serial.write(w2);
      Serial.write(",");
      int w3 = random(0,254);
      Serial.write("W3=");
      Serial.write(w3);
      Serial.write(",");
      int w4 = random(0,254);
      Serial.write("W4=");
      Serial.write(w4);
      Serial.write(",");
      int w5 = random(0,254);
      Serial.write("W5=");
      Serial.write(w5);
      Serial.write(",");
      int w6 = random(0,254);
      Serial.write("W6=");
      Serial.write(w6);
      Serial.write(",");
      int w7 = random(0,254);
      Serial.write("W7=");
      Serial.write(w7);
      Serial.write(",");
      int w8 = random(0,254);
      Serial.write("W8=");
      Serial.write(w8);
      Serial.write(",");
      int w9 = random(0,254);
      Serial.write("W9=");
      Serial.write(w9);
      Serial.write(",");
      int w10 = random(0,254);
      Serial.write("W10=");
      Serial.write(w10);
      Serial.write(",");
      int w11 = random(0,254);
      Serial.write("W11=");
      Serial.write(w11);
      Serial.write('\n');
      delay(100);
      
    }else if (hold == "33") {
      int f1 = random(0,10);
      Serial.write("F1=");
      Serial.write(f1);
      Serial.write(",");
      int f2 = random(0,10);
      Serial.write("F2=");
      Serial.write(f2);
      Serial.write(",");
      int f3 = random(0,10);
      Serial.write("F3=");
      Serial.write(f3);
      Serial.write(",");
      int f4 = random(0,10);
      Serial.write("F4=");
      Serial.write(f4);
      Serial.write(",");
      int f5 = random(0,10);
      Serial.write("F5=");
      Serial.write(f5);
      Serial.write(",");
      int f6 = random(0,10);
      Serial.write("F6=");
      Serial.write(f6);
      int b1 = random(0,254);
      Serial.write("B1=");
      Serial.write(b1);
      Serial.write('\n');
      delay(100);  
    }
  }
}


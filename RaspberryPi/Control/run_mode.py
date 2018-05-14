#*********************************************************************
#Run Mode V_01
#Authors:Jake Smiley & Ben Bellerose & Steven Kalapos
#Description: This is where all outputs to devices are handled
#*********************************************************************
import serial
import RPi.GPIO as GPIO
import time
from time import gmtime,strftime

#Communication with arduino displaying our sensors
def read_sensor():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        hold1 = ser.readline().replace("\r", "")
        hold1 = hold1.replace("\n", "")
        hold1 = hold1.split("-")
        bank = []
        x = 0
        while x < len(hold1):
            hold = hold1[x].split("=")
            bank.insert(len(bank), hold)
            x = x + 1
    except Exception as e:
        print(e)
        bank = ["NA"]
    #print(hold1)
    return bank

#Find the sensor value by reading ardunio
def sensor_value(Sensor,Unit):
    try:
        x = 0
        values = read_sensor()
	    #print(values)
        while x < len(values):
            if values[x][0] == Sensor:
                sens_val = values[x][1].replace(Unit, "")
                sens_val = float(sens_val)
                x = len(values)
            x = x + 1
        return sens_val
    except Exception as e:
        #print(e)
        sens_val = "ERROR"

#PID controler that returns value of 0%-100%
def PID(SP,PV,Kp,Ki,Kd,I,E):
    E2 = E
    E = SP - PV
    I = I + E
    D = E - E2
    CV = (Kp*E)+(Ki*I)+(Kd*D)
    time.sleep(0.5)
    Output = (CV/SP)*100
    if Output > 100:
        Output = 100
    return Output,E

#Setup for raspberrypi gpio output
def InitalizeOut(Pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Pin, GPIO.OUT)
    GPIO.output(Pin, GPIO.HIGH) #Initalize as off
    time.sleep(0.5)
    return True

#Setup for raspberrypi gpio input
def InitalizeIn(Pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Pin, GPIO.IN)
    time.sleep(0.5)
    return True

#Power control for light
def Light(Pin, Light):
    InitalizeOut(Pin)

    #Handling of day Ligh
    Light_SP = int((float(Light)/(100.00))*(24.00))
    Hour = strftime("%H", gmtime())
    if Hour <= Light_SP:
        GPIO.output(Pin, GPIO.LOW)
        return True
    elif Hour > Light_SP:
        GPIO.output(Pin, GPIO.HIGH)
        return False

#Power control for pump
def Pump(P_Pin, WS_Pin):
    InitalizeOut(P_Pin)
    InitalizeIn(WS_Pin)

    #Handaling of water pumps
    if GPIO.input(WS_Pin):
        GPIO.output(P_Pin, GPIO.HIGH)
        return False
    else:
        GPIO.output(P_Pin, GPIO.LOW)
        return True

#Power control for mister
def Mister(Pin, Humidity, Humidity_SP):
    InitalizeOut(Pin)

    if int(Humidity) < int(Humidity_SP):
        GPIO.output(Pin, True)
        return True
    else:
        GPIO.output(Pin, False)
        return False

#Power control for fan
def Fan(Pin, Output):
    InitalizeOut(Pin)

    #Handling of fan
    if Output == True:
        GPIO.output(Pin, GPIO.LOW)
        return True
    elif Output == False:
        GPIO.output(Pin, GPIO.HIGH)
        return False

#Power control for hot plate
def HotPlate(Pin, Output):
    InitalizeOut(Pin)

    #Handling of hot plate
    if Output == True:
        GPIO.output(Pin, GPIO.LOW)
        return True
    elif Output == False:
        GPIO.output(Pin, GPIO.HIGH)
        return False

if __name__ == "__main__":
    #Output Pin variables
    L1_Pin = 26 #Light GPIO 25
    P0_Pin = 9 #Main resevoir pump GPIO 13
    P1_Pin = 5 #Dosing pump GPIO 21
    P2_Pin = 13 #Dosing pump GPIO 23
    P3_Pin = 16 #Dosing pump GPIO 27
    P4_Pin = 1 #Dosing pump GPIO
    P5_Pin = 22 #Dosing pump GPIO 3
    P6_Pin = 27 #Dosing pump GPIO 2
    F1_Pin = 6 #Circulation fan GPIO 22
    F2_Pin = 8 #Exhaust fan GPIO 10
    Drain_Pin =  19 #Drain solenoid GPIO 24
    Mister_Pin = 25 #Mister GPIO 6

    #Inputs
    T1 = sensor_value("T1","C")
    H1 = sensor_value("H1","%")
    WL1 = sensor_value("WL1","")
    F1 = sensor_value("F1","")

    #Processing of inputs
    Temp = T1
    Humid = H1

    #Output control
    Light(L1_Pin,Light)
    Mister(M1_Pin, True)
    Fan(F1_Pin, True)
    Fan(F2_Pin, True)
    Mister(Mister_Pin, Humid, Humidity_SP)

    #Pump(P0_Pin, WL1)
    #HotPlate(HP1_Pin, True)

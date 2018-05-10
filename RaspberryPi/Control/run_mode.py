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
    ser = serial.Serial('/dev/ttyACM0', 9600)
    hold1 = ser.readline().replace("\r", "")
    hold2 = ser.readline().replace("\r", "")
    hold3 = ser.readline().replace("\r", "")
    hold1 = hold1.replace("\n", "")
    hold2 = hold2.replace("\n", "")
    hold3 = hold3.replace("\n", "")
    hold1 = hold1.split("=")
    hold2 = hold2.split("=")
    hold3 = hold3.split("=")
    return hold1, hold2, hold3

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
    except:
        #print("error reading " + str(Sensor))
        return "ERROR"

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

#Setup for raspberrypi gpio output
def InitalizeIn(Pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Pin, GPIO.IN)
    time.sleep(0.5)
    return True

#Power control for light
def Light(Pin, Light):
    Pin = 13 #Hard coded overwrite
    Light = 100 #Hard coded overwrite
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
    WS_Pin = 5 #Hard coded overwrite
    P_Pin = 6 #Hard coded overwrite
    InitalizeOut(P_Pin)
    InitalizeIn(WS_Pin)

    #Handaling of water pumps
    if GPIO.input(WS_Pin):
        GPIO.output(P_Pin, GPIO.HIGH)
        return False
    else:
        GPIO.output(P_Pin, GPIO.LOW)
        return True

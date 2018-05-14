#*********************************************************************
#Cheech V_01
#Authors:Jake Smiley & Ben Bellerose & Steven Kalapos
#Description: Main control for Ecozone
#*********************************************************************
import os
import sys
import time
from time import gmtime,strftime
import csv
import serial
import RPi.GPIO as GPIO
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

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

#Controler for the fan
def Fan(SP,I,E):
    sensor = read_sensor()
    PV = sensor[1][1].replace("C", "")
    PV = PV.replace("%", "")
    PV = float(PV)
    #print(PV)
    Kp = 1.00
    Ki = 0.02
    Kd = 0.01
    Output = PID(SP,PV,Kp,Ki,Kd,I,E)
    E = Output[1]
    return(Output[0],I,Output[1])

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

#Find the temp from reading
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
        sens_val = "ERROR"


#Reads values from a csv file
def read_csv(CSV_File):
    External_txt = ''
    File = os.getcwd() + "/" + CSV_File
    External_txt = open(File, "r")
    External_txt = csv.reader(External_txt)
    External_txt = list(External_txt)
    del External_txt[0]
    return External_txt

#Writes to csv file
def input_csv(Content, CSV_File):
    if len(Content) >= 1:
        with open(CSV_File, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)
            x = 0
            while x < len(Content):
                a = 0
                Hold = []
                while a < len(Content[x]):
                    Hold.insert(len(Hold),Content[x][a])
                    a = a + 1
                spamwriter.writerow(Hold)
                x = x + 1
        return("Input Complete")
    else:
        return("Error With Input")

if __name__ == "__main__":
    #Pin variables
    L_Pin = 26 #Light GPIO 25
    P_Pin = 9 #Pump GPIO 13
    Fan1_Pin = 6 #Circulation fan GPIO 22
    Fan2_Pin = 8 #Exhaust fan GPIO 10
    DPump1_Pin = 5 #Dosing pump GPIO 21
    DPump2_Pin = 13 #Dosing pump GPIO 23
    DPump3_Pin = 16 #Dosing pump GPIO 27
    DPump4_Pin = 1 #Dosing pump GPIO
    DPump5_Pin = 22 #Dosing pump GPIO 3
    DPump6_Pin = 27 #Dosing pump GPIO 2
    Drain_Pin =  19 #Drain solenoid GPIO 24
    Mister_Pin = 25 #Mister GPIO 6

    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)
    GPIO.setup(L_Pin, GPIO.OUT)
    GPIO.setup(P_Pin, GPIO.OUT)
    GPIO.setup(Fan1_Pin, GPIO.OUT)
    GPIO.setup(Fan2_Pin, GPIO.OUT)
    GPIO.setup(DPump1_Pin, GPIO.OUT)
    GPIO.setup(DPump2_Pin, GPIO.OUT)
    GPIO.setup(DPump3_Pin, GPIO.OUT)
    GPIO.setup(DPump4_Pin, GPIO.OUT)
    GPIO.setup(DPump5_Pin, GPIO.OUT)
    GPIO.setup(DPump6_Pin, GPIO.OUT)
    GPIO.setup(Drain_Pin, GPIO.OUT)
    GPIO.setup(Mister_Pin, GPIO.OUT)

    #Initalize outputs as off
    GPIO.output(L_Pin, False)
    GPIO.output(P_Pin, False)
    GPIO.output(Fan1_Pin, False)
    GPIO.output(Fan2_Pin, False)
    GPIO.output(DPump1_Pin, False)
    GPIO.output(DPump2_Pin, False)
    GPIO.output(DPump3_Pin, False)
    GPIO.output(DPump4_Pin, False)
    GPIO.output(DPump5_Pin, False)
    GPIO.output(DPump6_Pin, False)
    GPIO.output(Drain_Pin, False)
    GPIO.output(Mister_Pin, False)
    delay = 5
    max_sleep = 5
    time.sleep(0.5)

    #Main control loop
    try:
        while True:
            #Read main control file
            Homedir = os.getcwd() + "/"
            Power_File = open(Homedir + "control_files/power_control.txt", "r")
            File_Hold = Power_File.readlines()
            Power = File_Hold[0].split("-")
            #If power of OFF
            if Power[0] == "0":
                print("OFF")
                time.sleep(delay)
            #If power is ON
            elif Power[0] == "1":
                print("ON")
                #Read and parse sensor data
                Date = strftime("%Y-%m-%d", gmtime())
                Read_Control = open(Homedir + "control_files/index_control.txt", "r")
                Control = Read_Control.readlines()
                Read_Control.close()
                Control[0] = Control[0].replace("\n","")
                #print(Control)

                #Day log verification
                if str(Control[0]) != str(Date):
                    Date_Hold = Control[0].split("-")
                    Today_Hold = Date.split("-")
                    Year_Diff = int(Today_Hold[0])-int(Date_Hold[0])
                    Month_Diff = int(Today_Hold[1])-int(Date_Hold[1])
                    Day_Diff = int(Today_Hold[2])-int(Date_Hold[2])
                    Write_Control = open("control_files/index_control.txt", "w")
                    #If difference in days is less then 5 fill in missing days from log
                    if int(Day_Diff) < max_sleep:
                        #print(str(Year_Diff)+str(Month_Diff)+str(Day_Diff))
                        x = 0
                        Write_Control.write(Date)
                        Write_Control.write("\n")
                        while x < Day_Diff:
                            Count = int(Today_Hold[2]) - x - 1
                            Count_Hold = str(Today_Hold[0]) + "-" + str(Today_Hold[1]) + "-" + str(Count)
                            Write_Control.write(Count_Hold)
                            Write_Control.write("\n")
                            x = x +  1
                        a = 1
                        while a < len(Control):
                            Write_Control.write(str(Control[a]))
                            Write_Control.write("\n")
                            a = a + 1
                        Write_Control.close()
                    #If difference is greater than 5 start the schedule over in the log
                    else:
                        Write_Control.write(Date)
                        Write_Control.write("\n")
                        Write_Control.close()

                #Determine what day in the schedule your on
                Read_Control = open(Homedir + "control_files/index_control.txt", "r")
                Control = Read_Control.readlines()
                Read_Control.close()
                Index = len(Control)-1

                #Manual mode
                if Power[1] == "0":
                    print("Manual")

                    #Find SP values from user
                    Schedule = read_csv("control_files/manual_sp.csv")
                    Day = "NA"
                    Temp_SP = Schedule[1][1]
                    Humidity_SP = Schedule[1][2]
                    Light = Schedule[1][3]

                #Auto mode
                elif Power[1] == "1":
                    print("Auto")

                    #Find index SP values from schedule
                    Schedule = read_csv("control_files/schedule.csv")
                    Day = Schedule[Index][0]
                    Temp_SP = Schedule[Index][1]
                    Humidity_SP = Schedule[Index][2]
                    Light = Schedule[Index][3]

                #Read sensor values
                T1 = sensor_value("T1","C")
                H1 = sensor_value("H1","%")
                WL1 = sensor_value("WL1","")
                F1 = sensor_value("F1","")

                #Processing of present values
                Temp = T1
                Humid = H1

                #Handling of day Light
                Light_SP = int((float(Light)/(100.00))*(24.00))
                Hour = strftime("%H", gmtime())
                if int(Hour) <= int(Light_SP):
                    GPIO.output(L_Pin, True)
                else:
                    GPIO.output(L_Pin, False)
                    Index = int(Index) + 1
                    if Power[1] == "1":
                        #Find index SP values from schedule
                        Schedule = read_csv("control_files/schedule.csv")
                        Day = Schedule[Index][0]
                        Temp_SP = Schedule[Index][1]
                        Humidity_SP = Schedule[Index][2]

		        #Handaling of mister
                if Humid is None:
                    GPIO.output(Mister_Pin, False)
                elif int(Humid) < int(Humidity_SP):
                    GPIO.output(Mister_Pin, True)
                else:
                    GPIO.output(Mister_Pin, False)

                #Handaling of water pumps
                if WL1 is None:
                    GPIO.output(P_Pin, False)
                elif WL1 > 330:
                    print("Full")
                    GPIO.output(P_Pin, False)
                else:
                    GPIO.output(P_Pin, True)

	            #Handling of fans
                GPIO.output(Fan1_Pin, True)
                GPIO.output(Fan2_Pin, True)

                #Printing of variables
                print(Date)
                print("Index = " + str(Day))
                print("Tempature = " + str(Temp) + "C")
                print("Humidity = " + str(Humid) + "%")
                print("Waterlevel = " + str(WL))
                print("Temp Setpoint = " + str(Temp_SP) + "C")
                print("Humidity Setpoint = " + str(Humidity_SP) + "%")
                print("Sunlight = " + str(Light_SP) + "hrs")
                time.sleep(delay)

    except KeyboardInterrupt or (raw_input().upper() == "END"):
        #Take Picture
        camera = PiCamera()
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        #Clear Outputs
        GPIO.cleanup()
        print("Unexpected Error")

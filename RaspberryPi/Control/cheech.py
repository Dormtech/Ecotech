#*********************************************************************
#Cheech V_01
#Authors:Jake Smiley & Ben Bellerose
#Description: Main control for Ecozone
#*********************************************************************
import os
import time
from time import gmtime,strftime
import csv
import serial
import RPi.GPIO as GPIO
#FUCK YOU STEVE
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
    except:
        #print("error reading " + str(Sensor))
        return "ERROR"

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

def index_verification(index_file):
    max_sleep = 5 #Number of day alowed to be off for before plant is dead
    Date = strftime("%Y-%m-%d", gmtime())
    Read_Control = open(index_file, "r")
    Control = Read_Control.readlines()
    Read_Control.close()
    Control[0] = Control[0].replace("\n","")

    #Day log verification
    if str(Control[0]) != str(Date):
        Date_Hold = Control[0].split("-")
        Today_Hold = Date.split("-")
        Year_Diff = int(Today_Hold[0])-int(Date_Hold[0])
        Month_Diff = int(Today_Hold[1])-int(Date_Hold[1])
        Day_Diff = int(Today_Hold[2])-int(Date_Hold[2])
        Write_Control = open(index_file, "w")
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

if __name__ == "__main__":
    #Pin variables
    L_Pin = 13 #Light
    P_Pin = 6 #Pump
    F_Pin = 7 #Fan
    WS_Pin = 5 #Water Sensor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(L_Pin, GPIO.OUT)
    GPIO.setup(P_Pin, GPIO.OUT)
    GPIO.setup(F_Pin, GPIO.OUT)
    GPIO.setup(WS_Pin, GPIO.IN)

    #Initalize outputs as off
    GPIO.output(L_Pin, GPIO.HIGH)
    GPIO.output(P_Pin, GPIO.HIGH)
    GPIO.output(F_Pin, GPIO.HIGH)
    delay = 5 #Cycle delay
    time.sleep(0.5)

    #Main control loop
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

            #Determine what day in the schedule your on
            index_verification("control_files/index_control.txt")
            Read_Control = open("control_files/index_control.txt", "r")
            Control = Read_Control.readlines()
            Read_Control.close()
            Index = len(Control)-1

            #Manual mode
            if Power[1] == "0":
                print("Manual")
                Schedule = read_csv("control_files/manual_sp.csv")

            #Auto mode
            elif Power[1] == "1":
                print("Auto")
                Schedule = read_csv("control_files/schedule.csv")

            #Find index SP values from schedule
            Temp_SP = Schedule[Index][1]
            Day = Schedule[Index][0]
            Humidity_SP = Schedule[Index][2]
            Light = Schedule[Index][3]

            #Read sensor values
            T1 = sensor_value("T1","C")
            H1 = sensor_value("H1","%")

            #Processing of present values
            Temp = T1
            Humid = H1

            #Handling of tempature
            Deadband = 5
            if Temp > Temp_SP:
                GPIO.output(F_Pin, GPIO.LOW)
            elif Temp <= Temp_SP:
                GPIO.output(F_Pin, GPIO.HIGH)

            #Handling of day Light
            Light_SP = int((float(Light)/(100.00))*(24.00))
            Hour = strftime("%H", gmtime())
            if Hour <= Light_SP:
                GPIO.output(L_Pin, GPIO.LOW)
            elif Hour > Light_SP:
                GPIO.output(L_Pin, GPIO.HIGH)

            #Handaling of water pumps
            if GPIO.input(WS_Pin):
                print("Full")
                GPIO.output(P_Pin, GPIO.HIGH)
            else:
                GPIO.output(P_Pin, GPIO.LOW)

            #Printing of variables
            print(Date)
            print("Index = " + str(Index))
            print("Tempature = " + str(Temp) + "C")
            print("Humidity = " + str(Humid) + "%")
            print("Temp Setpoint = " + str(Temp_SP) + "C")
            print("Humidity Setpoint = " + str(Humidity_SP) + "%")
            print("Sunlight = " + str(Light_SP) + "hrs")
            cur_val = [Power[0],Index,Dist,Temp,Humid,Temp_SP,Humidity_SP,Light_SP,len(Schedule)]
            val_export = [["Power","Index","Dist","Temp","Humid","Temp_SP","Humidity_SP","Light_SP","Cycle"],cur_val]
            input_csv(val_export,"control_files/current_values.csv")
            time.sleep(delay)

    print("unexpected error")

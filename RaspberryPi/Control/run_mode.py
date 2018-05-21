"""
 * @file run_mode.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified May 21 2018
 * @modifiedby Ben Bellerose
 * @brief contains various output controls for device
 */
 """
import serial
import RPi.GPIO as GPIO
import time
from time import gmtime,strftime

"""Input: no input needed for function
   Function: reads sensor values over serial communication
   Output: writes out array of values for all sensors or NA if there is a problem"""
def read_Sensor():
    try:
        if serial.Serial('/dev/ttyACM0', 9600):
            ser = serial.Serial('/dev/ttyACM0', 9600) #/dev/ttyACM0 location of serial device
            hold1 = ser.readline().replace("\r", "")
            hold1 = hold1.replace("\n", "")
            hold1 = hold1.split("-")
            bank = []
            x = 0
            while x < len(hold1):
                hold = hold1[x].split("=")
                bank.insert(len(bank), hold)
                x = x + 1
            return bank
        else:
            #print("ERROR READING SERIAL")
            bank = ["NA"]
            return bank
    except Exception as e:
        #Print("NO SERIAL CONNECTION")
        bank = ["NA"]
        return bank

"""Input: sensor - string containing the sensor you are trying to find
          unit - string containing the unit of the sensor you are looking for
   Function: finds your chosen sensor value from the sensor array
   Output: writes float value for the desired sensor or NA if there is a problem"""
def sensor_Value(sensor,unit):
    if sensor not None:
        if unit not None:
            try:
                values = read_Sensor()
                x = 0
        	    #print(values)
                while x < len(values):
                    if str(values[x][0]) == str(sensor):
                        sens_val = values[x][1].replace(str(unit), "")
                        sens_val = float(sens_val)
                        x = len(values)
                    else:
                        sens_val = "NA"
                    x = x + 1
                return sens_val
            except Exception as e:
                #print("ERROR FINDING SENSOR")
                sens_val = "ERROR"
                return sens_val
        else:
            #print("NO UNIT GIVEN")
            sens_val = "ERROR"
            return sens_val
    else:
        #print("NO SENSOR GIVEN")
        sens_val = "ERROR"
        return sens_val

"""Input: SP - integer containing the setpoint value
          PV - integer containing the present value
          Kp - integer containing the propotional weight value
          Ki - integer containing the integral weight value
          Kd - integer containing the derivetive weight value
          I - integer containing the integral value
          E - integer containing the error value
   Function: this is a PID control loop useful for fine tuning controls
   Output: writes out integer value between 0-100"""
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

"""Input: pin - integer value containing the desired pin
   Function: set a desired pin to an output
   Output: returns a boolean to inform user when done"""
def initalizeOut(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False) #Initalize as off
    time.sleep(0.5)
    return True

"""Input: pin - integer value containing the desired pin
   Function: set a desired pin to an input
   Output: returns a boolean to inform user when done"""
def initalizeIn(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    time.sleep(0.5)
    return True

"""Input: pin - integer value containing the light pin location
          light - float value containing the desired output time of light
   Function: controls output state of a light
   Output: returns a boolean to inform user of lights current state"""
def Light(pin, light):
    initalizeOut(pin)

    #Handling of day Ligh
    light_sp = int((float(light)/(100.00))*(24.00))
    hour = strftime("%H", gmtime())
    if hour <= light_sp:
        GPIO.output(pin, True)
        return True
    elif hour > light_sp:
        GPIO.output(pin, False)
        return False

"""Input: pin - integer value containing the pump pin location
          ws - integer value containing the current value of the water sensor
   Function: controls output state of a pump
   Output: returns a boolean to inform user of pumps current state"""
def Pump(pin, ws):
    initalizeOut(pin)

    #Handaling of water pumps
    if int(ws) >= 200:
        GPIO.output(pin, False)
        return False
    else:
        GPIO.output(pin, True)
        return True

"""Input: pin - integer value containing the mister pin location
          humidity - integer value containing the current humidity value
          humidity_sp - integer value containing the wanted humidity value
   Function: controls output state of a mister
   Output: returns a boolean to inform user of mister current state"""
def Mister(pin, humidity, humidity_sp):
    initalizeOut(pin)

    if int(humidity) < int(humidity_sp):
        GPIO.output(pin, True)
        return True
    else:
        GPIO.output(pin, False)
        return False

"""Input: pin - integer value containing the desired pin
          output - boolean value containing the desired output of the fan
   Function: controls output state of a fan
   Output: returns a boolean to inform user of fans current state"""
def Fan(pin, output):
    initalizeOut(pin)

    #Handling of fan
    if output == True:
        GPIO.output(pin, True)
        return True
    elif output == False:
        GPIO.output(pin, False)
        return False

"""Input: pin - integer value containing the desired pin
          output - boolean value containing the desired output of the fan
   Function: controls output state of a hotplate
   Output: returns a boolean to inform user of hotplates current state"""
def hotPlate(pin, output):
    initalizeOut(pin)

    #Handling of hot plate
    if output == True:
        GPIO.output(pin, GPIO.LOW)
        return True
    elif output == False:
        GPIO.output(pin, GPIO.HIGH)
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
    T1 = sensor_Value("T1","C")
    H1 = sensor_Value("H1","%")
    WL1 = sensor_Value("WL1","")
    F1 = sensor_Value("F1","")
    Light = 85

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
    #hotPlate(HP1_Pin, True)

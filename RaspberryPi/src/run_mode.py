"""
 * @file run_mode.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified May 21 2018
 * @modifiedby BB
 * @brief contains various output controls for device
 */
 """
import serial
import RPi.GPIO as GPIO
import time
from time import gmtime,strftime
from logg import deviceLog

class deviceControl():

    """Input: no input needed for function
       Function: reads sensor values over serial communication
       Output: writes out array of values for all sensors or NA if there is a problem"""
    def read_Sensor(self):
        if serial.Serial('/dev/ttyACM0', 9600):
            try:
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
            except Exception as e:
                deviceLog().errorLog("ERROR READING SERIAL",e)
                print("ERROR READING SERIAL")
                bank = ["NA"]
                return bank
        else:
            deviceLog().errorLog("NO SERIAL","Device unpluged.")
            print("NO SERIAL CONNECTION")
            bank = ["NA"]
            return bank

    """Input: sensor - string containing the sensor you are trying to find
              unit - string containing the unit of the sensor you are looking for
       Function: finds your chosen sensor value from the sensor array
       Output: writes float value for the desired sensor or NA if there is a problem"""
    def sensor_Value(self, sensor, unit):
        if sensor is not None:
            if unit is not None:
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
                    deviceLog().errorLog("ERROR FINDING SENSOR",e)
                    print("ERROR FINDING SENSOR")
                    sens_val = "ERROR"
                    return sens_val
            else:
                deviceLog().errorLog("NO UNIT GIVEN","No unit provided.")
                print("NO UNIT GIVEN")
                sens_val = "ERROR"
                return sens_val
        else:
            deviceLog().errorLog("NO SENSOR GIVEN","No sensor value provided.")
            print("NO SENSOR GIVEN")
            sens_val = "ERROR"
            return sens_val

    """Input: pin - integer value containing the desired pin
       Function: set a desired pin to an output
       Output: returns a boolean to inform user when done"""
    def initalizeOut(self, pin):
        if pin is not None:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, False) #Initalize as off
                time.sleep(0.5)
                return True
            except Exception as e:
                deviceLog().errorLog("ERROR INITALIZING OUTPUT","Unable to set GPIO pin as output.")
                print("ERROR INITALIZING OUTPUT")
                return False
        else:
            deviceLog().errorLog("NO PIN GIVEN","No pin value provided.")
            print("NO PIN GIVEN")
            return False

    """Input: pin - integer value containing the desired pin
       Function: set a desired pin to an input
       Output: returns a boolean to inform user when done"""
    def initalizeIn(self, pin):
        if pin is not None:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(pin, GPIO.IN)
                time.sleep(0.5)
                return True
            except Exception as e:
                deviceLog().errorLog("ERROR INITALIZING INPUT","Unable to set GPIO pin as input.")
                print("ERROR INITALIZING INPUT")
                return False
        else:
            deviceLog().errorLog("NO PIN GIVEN","No pin value provided.")
            print("NO PIN GIVEN")
            return False

    """Input: pin - integer value containing the light pin location
              light - float value containing the desired output time of light
       Function: controls output state of a light
       Output: returns a integer to inform user of lights current state"""
    def Light(self, pin, light):
        if pin is not None:
            if light is not None:
                init = initalizeOut(pin)
                if init == True:
                    try:
                        #Handling of day Ligh
                        light_sp = int((float(light)/(100.00))*(24.00))
                        hour = strftime("%H", gmtime())
                        if hour <= light_sp:
                            GPIO.output(pin, True)
                            return 0 #ON
                        elif hour > light_sp:
                            GPIO.output(pin, False)
                            return 1 #OFF
                    except Exception as e:
                        deviceLog().errorLog("ERROR CONTROLING LIGHT","Error occured when trying to control light.")
                        print("ERROR CONTROLING LIGHT")
                        return 2 #ERROR
                else:
                    #Could not initalize
                    return 2 #ERROR
            else:
                deviceLog().errorLog("NO LIGHT VALUE GIVEN","No light value was provided.")
                print("NO LIGHT VALUE GIVEN")
                return 2 #ERROR
        else:
            deviceLog().errorLog("NO PIN GIVEN","No pin value provided.")
            print("NO PIN GIVEN")
            return 2 #ERROR

    """Input: pin - integer value containing the pump pin location
              ws - integer value containing the current value of the water sensor
       Function: controls output state of a pump
       Output: returns a integer to inform user of pumps current state"""
    def Pump(self,pin, ws):
        if pin is not None:
            if ws is not None:
                init = initalizeOut(pin)
                if init == True:
                    try:
                        #Handaling of water pumps
                        if int(ws) >= 200:
                            GPIO.output(pin, False)
                            return 1 #OFF
                        else:
                            GPIO.output(pin, True)
                            return 0 #ON
                    except Exception as e:
                        deviceLog().errorLog("ERROR CONTROLING PUMP","Error occured when trying to control pump.")
                        print("ERROR CONTROLING PUMP")
                        return 2 #ERROR
                else:
                    #Could not initalize
                    return 2 #ERROR
            else:
                deviceLog().errorLog("NO WATER SENSOR GIVEN","No water sensor value was provided.")
                print("NO WATER SENSOR GIVEN")
                return 2 #ERROR
        else:
            deviceLog().errorLog("NO PIN GIVEN","No pin value provided.")
            print("NO PIN GIVEN")
            return 2 #ERROR

    """Input: pin - integer value containing the mister pin location
              humidity - integer value containing the current humidity value
              humidity_sp - integer value containing the wanted humidity value
       Function: controls output state of a mister
       Output: returns a integer to inform user of mister current state"""
    def Mister(self, pin, humidity, humidity_sp):
        if pin is not None:
            if humidity is not None:
                if humidity_sp is not None:
                    init = initalizeOut(pin)
                    if init == True:
                        try:
                            if int(humidity) < int(humidity_sp):
                                GPIO.output(pin, True)
                                return 0 #ON
                            else:
                                GPIO.output(pin, False)
                                return 1 #OFF
                        except Exception as e:
                            deviceLog().errorLog("ERROR CONTROLING MISTER","Error occured when trying to control the mister.")
                            print("ERROR CONTROLING MISTER")
                            return 2 #ERROR
                    else:
                        #Could not initalize
                        return 2 #ERROR
                else:
                    deviceLog().errorLog("NO HUMIDITY SETPOINT GIVEN","No humidity setpoint value was provided.")
                    print("NO HUMIDITY SETPOINT GIVEN")
                    return 2 #ERROR
            else:
                deviceLog().errorLog("NO HUMIDITY GIVEN","No humidity value was provided.")
                print("NO HUMIDITY GIVEN")
                return 2 #ERROR
        else:
            deviceLog().errorLog("NO PIN GIVEN","No pin value provided.")
            print("NO PIN GIVEN")
            return 2 #ERROR

    """Input: pin - integer value containing the desired pin
              output - boolean value containing the desired output of the fan
       Function: controls output state of a fan
       Output: returns a integer to inform user of fans current state"""
    def Fan(self, pin, output):
        if pin is not None:
            if output is not None:
                init = initalizeOut(pin)
                if init == True:
                    try:
                        #Handling of fan
                        if output == True:
                            GPIO.output(pin, True)
                            return 0 #ON
                        elif output == False:
                            GPIO.output(pin, False)
                            return 1 #OFF
                    except Exception as e:
                        deviceLog().errorLog("ERROR CONTROLING FAN","Error occured when trying to control fan.")
                        print("ERROR CONTROLING FAN")
                        return 2 #ERROR
                else:
                    #Could not initalize
                    return 2 #ERROR
            else:
                deviceLog().errorLog("NO OUTPUT STATE GIVEN","No output state was provided.")
                print("NO OUTPUT STATE GIVEN")
                return 2 #ERROR
        else:
            deviceLog().errorLog("NO PIN GIVEN","No pin value provided.")
            print("NO PIN GIVEN")
            return 2 #ERROR

    """Input: pin - integer value containing the desired pin
              output - boolean value containing the desired output of the fan
       Function: controls output state of a hotplate
       Output: returns a integer to inform user of hotplates current state"""
    def hotPlate(self, pin, output):
        if pin is not None:
            if output is not None:
                init = initalizeOut(pin)
                if init == True:
                    try:
                        #Handling of hot plate
                        if output == True:
                            GPIO.output(pin, GPIO.LOW)
                            return 0 #ON
                        elif output == False:
                            GPIO.output(pin, GPIO.HIGH)
                            return 1 #OFF
                    except Exception as e:
                        deviceLog().errorLog("ERROR CONTROLING HOTPLATE","Error occured when trying to control hotplate.")
                        print("ERROR CONTROLING HOTPLATE")
                        return 2 #ERROR
                else:
                    #Could not initalize
                    return 2 #ERROR
            else:
                deviceLog().errorLog("NO OUTPUT STATE GIVEN","No output state was provided.")
                print("NO OUTPUT STATE GIVEN")
                return 2 #ERROR
        else:
            deviceLog().errorLog("NO PIN GIVEN","No pin value provided.")
            print("NO PIN GIVEN")
            return 2 #ERROR

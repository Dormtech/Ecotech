"""
 * @file runMode.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified May 27 2018
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

    def __init__(self):
        self.hold1 = None
        GPIO.setwarnings(False)

    """Input: code - integer value regarding what sensors you want to read (1-3)
       Function: reads sensor values over serial communication
       Output: writes out array of values for all sensors or NA if there is a problem"""
    def readSensor(self, code):
        if code is not None:
            if serial.Serial('/dev/ttyUSB0', 9600):
                #ser = serial.Serial('/dev/ttyACM0', 9600) #/dev/ttyACM0 location of serial device
                ser = serial.Serial('/dev/ttyUSB0', 9600) #/dev/ttyUSB0 location of serial device
                time.sleep(1.7) #Magic wait time
                statusBit = str.encode(str(code) + "\r\n")
                ser.write(statusBit)
                time.sleep(0.1)
                hold1 = ser.readline()
                ser.reset_input_buffer()
                hold1 = str(hold1).replace("\\r", "")
                hold1 = hold1.replace("\\n", "")
                hold1 = hold1.replace("b'", "")
                hold1 = hold1.split(",")
                bank = []
                x = 0
                while x < len(hold1):
                    hold = hold1[x].split("=")
                    bank.insert(len(bank), hold)
                    x = x + 1
                return bank
            else:
                errCode = "NO SERIAL"
                errMsg = "No serial communication device unpluged."
                deviceLog().errorLog(errCode,errMsg)
                print("NO SERIAL CONNECTION")
                bank = ["ERROR"]
                return bank
        else:
            errCode = "NO CODE PROVIDED"
            errMsg = "No code was provided when checking serial port."
            deviceLog().errorLog(errCode,errMsg)
            print("NO CODE PROVIDED")
            bank = ["ERROR"]
            return bank

    """Input: sensor - string containing the sensor you are trying to find
              unit - string containing the unit of the sensor you are looking for
              bank - list of sensors and their values
       Function: finds your chosen sensor value from the sensor array
       Output: writes float value for the desired sensor or NA if there is a problem"""
    def sensorValue(self, sensor, unit, bank):
        if sensor is not None:
            if unit is not None:
                if bank is not None:
                    try:
                        x = 0
                	    #print(values)
                        while x < len(bank):
                            if str(bank[x][0]) == str(sensor):
                                sens_val = bank[x][1].replace(str(unit), "")
                                sens_val = float(sens_val)
                                x = len(bank)
                            else:
                                sens_val = "ERROR"
                            x = x + 1
                        return sens_val
                    except Exception as e:
                        errCode = "ERROR FINDING SENSOR"
                        errMsg = "Error finding sensor "+ str(sensor) + ". The following error code appeared; " + str(e)
                        deviceLog().errorLog(errCode,errMsg)
                        print("ERROR FINDING SENSOR")
                        sens_val = "ERROR"
                        return sens_val
                else:
                    errCode = "NO BANK GIVEN"
                    errMsg = "No bank provided for finding sensor " + str(sensor) + "."
                    deviceLog().errorLog(errCode,errMsg)
                    print("NO BANK GIVEN FOR SENSOR " + str(sensor))
                    sens_val = "ERROR"
                    return sens_val
            else:
                errCode = "NO UNIT GIVEN"
                errMsg = "No unit provided for sensor " + str(sensor) + "."
                deviceLog().errorLog(errCode,errMsg)
                print("NO UNIT GIVEN FOR SENSOR " + str(sensor))
                sens_val = "ERROR"
                return sens_val
        else:
            errCode = "NO SENSOR GIVEN"
            errMsg = "No sensor value provided."
            deviceLog().errorLog(errCode,errMsg)
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
                errCode = "ERROR INITALIZING OUTPUT"
                errMsg = "Unable to set GPIO pin " + str(pin) + " as output."
                deviceLog().errorLog(errCode,errMsg)
                print("ERROR INITALIZING OUTPUT")
                return False
        else:
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
                errCode = "ERROR INITALIZING INPUT"
                errMsg = "Unable to set GPIO pin " + str(pin) + " as input. The following error code appeared; " + str(e)
                deviceLog().errorLog(errCode,errMsg)
                print("ERROR INITALIZING INPUT")
                return False
        else:
            return False

    """Input: pin - integer value containing the light pin location
              light - float value containing the desired output time of light
       Function: controls output state of a light
       Output: returns a integer to inform user of lights current state"""
    def Light(self, pin, light):
        if pin is not None:
            if light is not None:
                init = self.initalizeOut(pin)
                if init == True:
                    try:
                        #Handling of day Ligh
                        light_sp = int((float(light)/(100.00))*(24.00))
                        hour = strftime("%H", gmtime())
                        if int(hour) <= light_sp:
                            GPIO.output(pin, True)
                            return 0 #ON
                        elif int(hour) > light_sp:
                            GPIO.output(pin, False)
                            return 1 #OFF
                    except Exception as e:
                        errCode = "ERROR CONTROLING LIGHT"
                        errMsg = "Error occured when trying to control light on GPIO pin " + str(pin) + ". The following error code appeared; " + str(e)
                        deviceLog().errorLog(errCode,errMsg)
                        print("ERROR CONTROLING LIGHT")
                        return 2 #ERROR
                else:
                    #Could not initalize
                    return 2 #ERROR
            else:
                errCode = "NO LIGHT VALUE GIVEN"
                errMsg = "No light value was provided on GPIO pin " + str(pin) + "."
                deviceLog().errorLog(errCode,errMsg)
                print("NO LIGHT VALUE GIVEN")
                return 2 #ERROR
        else:
            errCode = "NO PIN GIVEN"
            errMsg = "No pin value provided for the light."
            deviceLog().errorLog(errCode,errMsg)
            print("NO PIN GIVEN FOR THE LIGHT")
            return 2 #ERROR

    """Input: pin - integer value containing the pump pin location
              ws - integer value containing the current value of the water sensor
       Function: controls output state of a pump
       Output: returns a integer to inform user of pumps current state"""
    def Pump(self,pin, ws):
        if pin is not None:
            if ws is not None:
                init = self.initalizeOut(pin)
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
                        errCode = "ERROR CONTROLING PUMP"
                        errMsg = "Error occured when trying to control pump on GPIO pin " + str(pin) + ". The following error code appeared; " + str(e)
                        deviceLog().errorLog(errCode,errMsg)
                        print("ERROR CONTROLING PUMP")
                        return 2 #ERROR
                else:
                    #Could not initalize
                    return 2 #ERROR
            else:
                errCode = "NO WATER SENSOR GIVEN"
                errMsg = "No water sensor value was provided for GPIO pin " + str(pin) + "."
                deviceLog().errorLog(errCode,errMsg)
                print("NO WATER SENSOR GIVEN")
                return 2 #ERROR
        else:
            errCode = "NO PIN GIVEN"
            errMsg = "No pin value provided for the pump."
            deviceLog().errorLog(errCode,errMsg)
            print("NO PIN GIVEN FOR THE PUMP")
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
                    init = self.initalizeOut(pin)
                    if init == True:
                        try:
                            if int(humidity) < int(humidity_sp):
                                GPIO.output(pin, True)
                                return 0 #ON
                            else:
                                GPIO.output(pin, False)
                                return 1 #OFF
                        except Exception as e:
                            errCode = "ERROR CONTROLING MISTER"
                            errMsg = "Error occured when trying to control the mister on GPIO pin " + str(pin) + ". The following error code appeared; " + str(e)
                            deviceLog().errorLog(errCode,errMsg)
                            print("ERROR CONTROLING MISTER")
                            return 2 #ERROR
                    else:
                        #Could not initalize
                        return 2 #ERROR
                else:
                    errCode = "NO HUMIDITY SETPOINT GIVEN"
                    errMsg = "No humidity setpoint value was provided for GPIO pin " + str(pin) + "."
                    deviceLog().errorLog(errCode,errMsg)
                    print("NO HUMIDITY SETPOINT GIVEN")
                    return 2 #ERROR
            else:
                errCode = "NO HUMIDITY GIVEN"
                errMsg = "No humidity value was provided " + str(pin) + "."
                deviceLog().errorLog(errCode,errMsg)
                print("NO HUMIDITY GIVEN")
                return 2 #ERROR
        else:
            errCode = "NO PIN GIVEN"
            errMsg = "No pin value provided for the mister."
            deviceLog().errorLog(errCode,errMsg)
            print("NO PIN GIVEN FOR THE MISTER")
            return 2 #ERROR

    """Input: pin - integer value containing the desired pin
              output - boolean value containing the desired output of the fan
       Function: controls output state of a fan
       Output: returns a integer to inform user of fans current state"""
    def Fan(self, pin, output):
        if pin is not None:
            if output is not None:
                init = self.initalizeOut(pin)
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
                        errCode = "ERROR CONTROLING FAN"
                        errMsg = "Error occured when trying to control fan on GPIO pin " + str(pin) + ". The following error code appeared; " + str(e)
                        deviceLog().errorLog(errCode,errMsg)
                        print("ERROR CONTROLING FAN")
                        return 2 #ERROR
                else:
                    #Could not initalize
                    return 2 #ERROR
            else:
                errCode = "NO OUTPUT STATE GIVEN"
                errMsg = "No output state was provided for GPIO pin " + str(pin) + "."
                deviceLog().errorLog(errCode,errMsg)
                print("NO OUTPUT STATE GIVEN")
                return 2 #ERROR
        else:
            errCode = "NO PIN GIVEN"
            errMsg = "No pin value provided for the fan."
            deviceLog().errorLog(errCode,errMsg)
            print("NO PIN GIVEN FOR THE FAN")
            return 2 #ERROR

    """Input: pin - integer value containing the desired pin
              output - boolean value containing the desired output of the fan
       Function: controls output state of a hotplate
       Output: returns a integer to inform user of hotplates current state"""
    def hotPlate(self, pin, output):
        if pin is not None:
            if output is not None:
                init = self.initalizeOut(pin)
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
                        errCode = "ERROR CONTROLING HOTPLATE"
                        errMsg = "Error occured when trying to control hotplate on GPIO pin " + str(pin) + ". The following error code appeared; " + str(e)
                        deviceLog().errorLog(errCode,errMsg)
                        print("ERROR CONTROLING HOTPLATE")
                        return 2 #ERROR
                else:
                    #Could not initalize
                    return 2 #ERROR
            else:
                errCode = "NO OUTPUT STATE GIVEN"
                errMsg = "No output state was provided for GPIO pin " + str(pin) + "."
                deviceLog().errorLog(errCode,errMsg)
                print("NO OUTPUT STATE GIVEN")
                return 2 #ERROR
        else:
            errCode = "NO PIN GIVEN"
            errMsg = "No pin value provided for the hotplate."
            deviceLog().errorLog(errCode,errMsg)
            print("NO PIN GIVEN FOR THE HOTPLATE")
            return 2 #ERROR

    """Input: sensor - string containing
       Function: shuts down all GPIO outputs in a case of a fire
       Output: returns a boolean to inform user of function state"""
    def Fire(self, sensor):
        errCode = "FIRE"
        errMsg = "Fire was detected with fire sensor " + str(sensor)
        deviceLog().errorLog(errCode,errMsg)
        GPIO.cleanup()
        return True

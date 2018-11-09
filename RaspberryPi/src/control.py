"""
 * @file control.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 21 2018
 * @modified November 8 2018
 * @modifiedby BB
 * @brief contains various output controls for device
 */
 """
import RPi.GPIO as GPIO
import time, os
from time import gmtime,strftime
from logg import deviceLog
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

class deviceControl():

    def __init__(self):
        GPIO.setwarnings(False)

    """Input: sensor - string containing the sensor you are trying to find
              unit - string containing the unit of the sensor you are looking for
              reading - bytes containg sensor values
       Function: finds your chosen sensor value from the sensor array
       Output: writes float value for the desired sensor or NA if there is a problem"""
    def sensorValue(self,sensor,unit,reading):
        if sensor is not None:
            if unit is not None:
                if reading is not None:
                    try:
                        #Processing of serial
                        reading = reading.decode("utf-8").replace("\\r", "")
                        reading = reading.replace("\\n'", "")
                        reading = reading.replace("b'", "")
                        reading = reading.split(",")
                        bank = []
                        for line in reading:
                            hold = line.split("=")
                            bank.insert(len(bank),hold)

                        #Parsing of data for sensor value
                        for value in bank:
                            if str(value[0]) == str(sensor):
                                sens_val = float(value[1].replace(str(unit), ""))
                                break
                            else:
                                sens_val = "ERROR"
                        return sens_val
                    except Exception as e:
                        errCode = "ERROR FINDING SENSOR"
                        errMsg = "Error finding sensor "+ str(sensor) + ". The following error code appeared; " + str(e)
                        deviceLog().errorLog(errCode,errMsg)
                        print("ERROR FINDING SENSOR")
                        sens_val = "ERROR"
                        return sens_val
                else:
                    errCode = "NO READING GIVEN"
                    errMsg = "No reading provided for finding sensor " + str(sensor) + "."
                    deviceLog().errorLog(errCode,errMsg)
                    print("NO READING GIVEN FOR SENSOR " + str(sensor))
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
    def initalizeOut(self,pin):
        if pin is not None:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, False) #Initalize as off
                time.sleep(0.1)
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
    def initalizeIn(self,pin):
        if pin is not None:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(pin, GPIO.IN)
                time.sleep(0.1)
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
              light - list containing offset (hrs) and amount of day light (hrs)
       Function: controls output state of a light
       Output: returns a integer to inform user of lights current state"""
    def Light(self,pin,light):
        if pin is not None:
            if light is not None:
                init = self.initalizeOut(pin)
                if init == True:
                    try:
                        #Handling of day Ligh
                        light = light.split(",")
                        offset = light[0]
                        dayLight = light[1]
                        lightEnd = int(offset) + int(dayLight)
                        hour = strftime("%H", gmtime())
                        if int(hour) > int(offset) and int(hour) <= int(lightEnd):
                            GPIO.output(pin, True)
                            return 0 #ON
                        else:
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
              amount - real value (L) containing the wanted amount of liquid from the pump
              flowRate - real value (L/min) containing the pumps flow rate
       Function: controls output state of a pump
       Output: returns a integer to inform user of pumps current state"""
    def Pump(self,pin,ws,amount,flowRate):
        if pin is not None:
            if ws is not None:
                init = self.initalizeOut(pin)
                if init == True:
                    try:
                        #Handaling of water pumps
                        if int(ws) >= 200:
                            runTime = time.time() + (60.00 * (float(amount)/float(flowRate)))
                            while time.time() <= runTime:
                                GPIO.output(pin, True)
                            return 0 #ON
                        else:
                            GPIO.output(pin, False)
                            return 1 #OFF
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
    def Mister(self,pin,humidity,humidity_sp):
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
    def Fan(self,pin,output):
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
    def hotPlate(self,pin,output):
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
    def Fire(sensor):
        errCode = "FIRE"
        errMsg = "Fire was detected with fire sensor " + str(sensor)
        deviceLog().errorLog(errCode,errMsg)
        GPIO.cleanup()
        return True

    """Input: fileName - string value containing the name you wish to save photo as
        Function: takes and saves picture of plant
        Output: returns a boolean value to inform user of machine state"""
    def captureIMG(fileName):
        if fileName is not None:
            if os.path.isfile(fileName):
                os.remove(fileName)
                time.sleep(0.1)
            cameraPi = PiCamera()
            rawCapture = PiRGBArray(cameraPi)
            time.sleep(0.1)
            cameraPi.capture(rawCapture, format="bgr")
            image = rawCapture.array
            cv2.imwrite(fileName,image)
            cameraPi.close()
            return True
        else:
            errCode = "NO FILE NAME PROVIDED"
            errMsg = "No file name was provided for the photo to be saved as."
            deviceLog().errorLog(errCode,errMsg)
            print("NO FILE NAME PROVIDED")
            return False

    """Input: valueBank - list containing all values to include in calculation
              weightBank - list containing all weights for the calculation
        Function: determines the weighted average of given values
        Output: returns a real value containing the weighted average"""
    def wAverage(self,valueBank,weightBank):
        if valueBank is not None:
            if weightBank is not None:
                if len(valueBank) == len(weightBank):
                    count = 0
                    value = 0
                    for x in range(len(valueBank)):
                        if type(valueBank[x]) is not str:
                            try:
                                value = value + (int(valueBank[x]) * weightBank[x])
                                count = count + 1
                            except:
                                pass
                    if count == 0:
                        value = "NA"
                        errCode = "SYSTEM FAILURE"
                        errMsg = "Unable to process values failed while calculating weighted average for valueBank " + str(valueBank) + "."
                        deviceLog().errorLog(errCode,errMsg)
                        print("SYSTEM FAILURE - CALCULATION FAILURE")
                    else:
                        value = value/count
                    return value
                else:
                    value = "NA"
                    errCode = "BANKS ARE NOT SAME LENGTH"
                    errMsg = "Banks supplied are different sizes."
                    deviceLog().errorLog(errCode,errMsg)
                    print("BANKS ARE NOT SAME LENGTH")
                    return value
            else:
                value = "NA"
                errCode = "NO WEIGHT BANK PROVIDED"
                errMsg = "No weight bank list was provided for the machine."
                deviceLog().errorLog(errCode,errMsg)
                print("NO WEIGHT BANK PROVIDED")
                return value
        else:
            value = "NA"
            errCode = "NO VALUE BANK PROVIDED"
            errMsg = "No value bank list was provided for the machine."
            deviceLog().errorLog(errCode,errMsg)
            print("NO VALUE BANK PROVIDED")
            return value

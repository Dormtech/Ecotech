"""
 * @file networking.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date July 12 2018
 * @modified July 16 2018
 * @modifiedby BB
 * @brief device network interactions
 */
 """
import os
import serial
import time
import subprocess
from logg import deviceLog

class network():

    """Input: no input needed for function
        Function: downloads most current version of code avalible
        Output: returns a boolean value to inform user if function was compleated"""
    def machineUpdate():
        if os.path.isdir("/home/pi/Desktop/Ecotech"):
            print("Updating device please wait.")
            os.chdir("/home/pi/Desktop/Ecotech")
            result1 = subprocess.run(['git','reset','--hard','origin/ben-testBranch'], stdout=subprocess.PIPE)
            result2 = subprocess.run(['git','pull','origin','ben-testBranch'], stdout=subprocess.PIPE)
            return True
        else:
            print("Downloadign source code please wait.")
            os.chdir("/home/pi/Desktop")
            result = subprocess.run(['git', 'clone', 'https://github.com/Dormtech/Ecotech.git'], stdout=subprocess.PIPE)
            return True

    """Input: no input needed for function
        Function: opens a serial port for serial communication
        Output: returns the open serial instance"""
    def openSerial():
        USB0 = '/dev/ttyACM0' #/dev/ttyACM0 location of serial device
        USB1 = '/dev/ttyUSB0' #/dev/ttyUSB0 location of serial device
        if os.path.exists(USB0):
            if serial.Serial(USB0):
                ser = serial.Serial(USB0, 9600, timeout=0.5)
                time.sleep(1.7)
                return ser
            else:
                errCode = "CONNECTION FAILURE"
                errMsg = "Serial device was unnable to connect with " + str(USB0)
                deviceLog().errorLog(errCode,errMsg)
                print("NO SERIAL CONNECTION")
                ser = None
                return ser
        elif os.path.exists(USB1):
            if serial.Serial(USB1):
                ser = serial.Serial(USB1, 9600, timeout=0.5)
                time.sleep(1.7)
                return ser
            else:
                errCode = "CONNECTION FAILURE"
                errMsg = "Serial device was unnable to connect with " + str(USB1)
                deviceLog().errorLog(errCode,errMsg)
                print("NO SERIAL CONNECTION")
                ser = None
                return ser
        else:
            errCode = "NO SERIAL"
            errMsg = "No serial communication device unpluged."
            deviceLog().errorLog(errCode,errMsg)
            print("NO SERIAL CONNECTION")
            ser = None
            return ser

    """Input: ser - open serial instance
        Function: closes open serial port
        Output: returns binary value indicating the outcome of the function"""
    def closeSerial(ser):
        if ser is not None:
            if ser.is_open():
                ser.close()
                time.sleep(0.5)
            else:
                print("SERIAL NOT OPEN")
                return False
        else:
            errCode = "NO SERIAL GIVEN"
            errMsg = "No serial value provided."
            deviceLog().errorLog(errCode,errMsg)
            print("NO SERIAL GIVEN")
            return False


    """Input: ser - open serial instance
              code - value (1-3) indicating what action serial device should preform
        Function: reads values from the serial port
        Output: returns bytes recived from serial device"""
    def readSerial(ser,code):
        if ser is not None:
            if ser.writable():
                #Read/Write serial
                ser.reset_output_buffer()
                statusBit = str.encode(str(code) + "\r\n")
                ser.write(statusBit)
                time.sleep(0.1)
                ser.reset_input_buffer()
                reading = ser.readline()
                time.sleep(0.1)
                return reading

            else:
                errCode = "SERIAL NOT WRITABLE"
                errMsg = "Serial device was not in a writable state"
                deviceLog().errorLog(errCode,errMsg)
                print("SERIAL NOT WRITABLE")
                reading = None
                return reading
        else:
            errCode = "NO SERIAL GIVEN"
            errMsg = "No serial value provided."
            deviceLog().errorLog(errCode,errMsg)
            print("NO SERIAL GIVEN")
            reading = None
            return reading

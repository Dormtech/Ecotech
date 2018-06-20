"""
 * @file pumpSequence.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified May 30 2018
 * @modifiedby BB
 * @brief control sequence for the pumps of the machine
 */
 """
from runMode import deviceControl

class pumps():

    """Input: no input needed for function
        Function: controls the atmosphere inside the machine
        Output: returns a boolean value to inform user of machine state"""
    def pumpMain(self,phSP):
        if phSP is not None:
            #Output Pin variable
            P0_Pin = 9 #Main resevoir pump GPIO 13
            P1_Pin = 5 #Dosing pump GPIO 21
            P2_Pin = 13 #Dosing pump GPIO 23
            P3_Pin = 16 #Dosing pump GPIO 27
            P4_Pin = 1 #Dosing pump GPIO
            P5_Pin = 22 #Dosing pump GPIO 3
            P6_Pin = 27 #Dosing pump GPIO 2
            Drain_Pin =  19 #Drain solenoid GPIO 24

            #Water level sensors
            if deviceControl().sensorValue("WL1","") == "ERROR":
                w1 = "NA"
            else:
                w1 = deviceControl().sensorValue("WL1","")
            if deviceControl().sensorValue("WL2","") == "ERROR":
                w2 = "NA"
            else:
                w2 = deviceControl().sensorValue("WL2","")
            if deviceControl().sensorValue("WL3","") == "ERROR":
                w3 = "NA"
            else:
                w3 = deviceControl().sensorValue("WL3","")
            if deviceControl().sensorValue("WL4","") == "ERROR":
                w4 = "NA"
            else:
                w4 = deviceControl().sensorValue("WL4","")
            if deviceControl().sensorValue("WL5","") == "ERROR":
                w5 = "NA"
            else:
                w5 = deviceControl().sensorValue("WL5","")
            if deviceControl().sensorValue("WL6","") == "ERROR":
                w6 = "NA"
            else:
                w6 = deviceControl().sensorValue("WL6","")
            if deviceControl().sensorValue("WL7","") == "ERROR":
                w7 = "NA"
            else:
                w7 = deviceControl().sensorValue("WL7","")
            if deviceControl().sensorValue("WL8","") == "ERROR":
                w8 = "NA"
            else:
                w8 = deviceControl().sensorValue("WL8","")
            if deviceControl().sensorValue("WL9","") == "ERROR":
                w9 = "NA"
            else:
                w9 = deviceControl().sensorValue("WL9","")

            #Fire sensors
            if deviceControl().sensorValue("F1","") == "ERROR":
                f1 = "NA"
            else:
                f1 = deviceControl().sensorValue("F1","")
            if deviceControl().sensorValue("F2","") == "ERROR":
                f2 = "NA"
            else:
                f2 = deviceControl().sensorValue("F2","")
            if deviceControl().sensorValue("F3","") == "ERROR":
                f3 = "NA"
            else:
                f3 = deviceControl().sensorValue("F3","")
            if deviceControl().sensorValue("F4","") == "ERROR":
                f4 = "NA"
            else:
                f4 = deviceControl().sensorValue("F4","")
            if deviceControl().sensorValue("F5","") == "ERROR":
                f5 = "NA"
            else:
                f5 = deviceControl().sensorValue("F5","")
            try:
                fire = int(f1) + int(f2) + int(f3) + int(f4) + int(f5) #Sum of fire sensors
            except:
                fire = "NA"
                print("SYSTEM FAILURE - FIRE SENSORS OFFLINE")

            #Output control
            fireLevel = 10
            if fire <= fireLevel and fire != "NA": #If fire is not detected
                return True

            elif fire > fireLevel and fire != "NA": #If fire is detected
                if f1 > fireLevel:
                    deviceControl().Fire("F1")
                elif f2 > fireLevel:
                    deviceControl().Fire("F2")
                elif f3 > fireLevel:
                    deviceControl().Fire("F3")
                elif f4 > fireLevel:
                    deviceControl().Fire("F4")
                elif f5> fireLevel:
                    deviceControl().Fire("F5")
                return False

            elif fire == "NA": #If all fire sensors are offline
                return False
        else:
            errCode = "NO PH SETPOINT PROVIDED"
            errMsg = "No ph setpoint value was provided for the machine."
            deviceLog().errorLog(errCode,errMsg)
            print("NO PH SETPOINT PROVIDED")
            return False

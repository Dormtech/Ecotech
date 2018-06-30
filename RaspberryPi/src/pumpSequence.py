"""
 * @file pumpSequence.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified June 20 2018
 * @modifiedby BB
 * @brief control sequence for the pumps of the machine
 */
 """
from runMode import deviceControl

class pumps():

    """Input: phSP - integer value containing the PH setpoint
        Function: controls the atmosphere inside the machine
        Output: returns a boolean value to inform user of machine state"""
    def pumpMain(self,phSP):
        if phSP is not None:
            #Output Pin variable
            P1_Pin = 13 #Main resevoir pump GPIO 23
            P2_Pin = 19 #Dosing pump GPIO 24
            P3_Pin = 26 #Dosing pump GPIO 25
            P4_Pin = 14 #Dosing pump GPIO 15
            P5_Pin = 15 #Dosing pump GPIO 16
            P6_Pin = 18 #Dosing pump GPIO 1
            P7_Pin = 23 #Dosing pump GPIO 4
            P8_Pin = 24 #Dosing pump GPIO 5
            P9_Pin = 25 #Dosing pump GPIO 6
            Drain_Pin =  12 #Drain solenoid GPIO 26

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
                if phSP > ph1 and ph1 != "NA": #PH level is low add nutrients
                    if w1 != "NA": #If tank 1 does not have errors
                        deviceControl().Pump(P1_Pin, w1) #Dispence pump
                        print("PUMP 1 ON")
                    elif w1 == "NA": #w1 sensor is not avalible
                        print("ERROR WITH W1")

                    if w2 != "NA": #If tank 2 does not have errors
                        deviceControl().Pump(P2_Pin, w2) #Dispence pump
                        print("PUMP 2 ON")
                    elif w2 == "NA": #w2 sensor is not avalible
                        print("ERROR WITH W2")

                    if w3 != "NA": #If tank 3 does not have errors
                        deviceControl().Pump(P3_Pin, w3) #Dispence pump
                        print("PUMP 3 ON")
                    elif w3 == "NA": #w3 sensor is not avalible
                        print("ERROR WITH W3")

                    if w4 != "NA": #If tank 4 does not have errors
                        deviceControl().Pump(P4_Pin, w4) #Dispence pump
                        print("PUMP 4 ON")
                    elif w4 == "NA": #w4 sensor is not avalible
                        print("ERROR WITH W4")

                    if w5 != "NA": #If tank 5 does not have errors
                        deviceControl().Pump(P5_Pin, w5) #Dispence pump
                        print("PUMP 5 ON")
                    elif w5 == "NA": #w5 sensor is not avalible
                        print("ERROR WITH W5")

                    if w6 != "NA": #If tank 6 does not have errors
                        deviceControl().Pump(P6_Pin, w6) #Dispence pump
                        print("PUMP 6 ON")
                    elif w6 == "NA": #w6 sensor is not avalible
                        print("ERROR WITH W6")

                    if w7 != "NA": #If tank 7 does not have errors
                        deviceControl().Pump(P7_Pin, w7) #Dispence pump
                        print("PUMP 7 ON")
                    elif w7 == "NA": #w7 sensor is not avalible
                        print("ERROR WITH W7")
                    return True

                elif phSP < ph1 and ph1 != "NA": #PH is to high add diluter
                    if w8 != "NA": #If tank 8 does not have errors
                        deviceControl().Pump(P8_Pin, w8) #Dispence pump
                        print("PUMP 8 ON")
                    elif w8 == "NA": #w8 sensor is not avalible
                        print("ERROR WITH W8")
                    return True

                elif phSP == ph1 and ph1 != "NA": #PH is right pump main resevoir
                    if w9 != "NA": #If tank 9 does not have errors
                        deviceControl().Pump(P9_Pin, w9) #Dispence pump
                        print("PUMP 9 ON")
                    elif w9 == "NA": #w9 sensor is not avalible
                        print("ERROR WITH W9")
                    return True

                elif ph1 == "NA":
                    return False

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

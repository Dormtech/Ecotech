"""
 * @file pumpSequence.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified July 30 2018
 * @modifiedby BB
 * @brief control sequence for the pumps of the machine
 */
 """
from control import deviceControl

class pumps():

    """Input: phSP - integer value containing the PH setpoint
              ser - open serial instance
        Function: controls the atmosphere inside the machine
        Output: returns a boolean value to inform user of machine state"""
    def pumpMain(self,phSP,ser):
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
            sensorBank2 = network.readSerial(ser,2)
            sensorBank3 = network.readSerial(ser,3)

            #Water level sensors
            wlBank = deviceControl().sensBank("WL","C",9,sensorBank2)

            #Fire sensors
            fBank = deviceControl().sensBank("F","",5,sensorBank3)
            try:
                fire = 0
                for x in range(fBank):
                    fire = fire + fBank[x]
                print("Fire levels are = " + str(fire))
            except:
                fire = "NA"
                print("SYSTEM FAILURE - FIRE SENSORS OFFLINE")

            #Output control
            fireLevel = 10
            if fire <= fireLevel and fire != "NA": #If fire is not detected
                
            elif fire > fireLevel and fire != "NA": #If fire is detected
                if int(fBank[0]) > fireLevel:
                    deviceControl().Fire("F1")
                elif int(fBank[1]) > fireLevel:
                    deviceControl().Fire("F2")
                elif int(fBank[2]) > fireLevel:
                    deviceControl().Fire("F3")
                elif int(fBank[3]) > fireLevel:
                    deviceControl().Fire("F4")
                elif int(fBank[4]) > fireLevel:
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

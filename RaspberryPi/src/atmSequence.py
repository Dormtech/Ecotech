"""
 * @file atmSequence.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified May 30 2018
 * @modifiedby BB
 * @brief control sequence for the atmosphere of the machine
 */
 """
from runMode import deviceControl

class atmosphere():

    """Input: humiditySP - integer value containing the humidity setpoint
              carbonSP - integer value containing the carbon setpoint
              tempatureSP - integer value containing the tempature setpoint in degrees celsius
              light - integer value 0-100 describing the percentage of ligth needed for the day
        Function: controls the atmosphere inside the machine
        Output: returns a boolean value to inform user of machine state"""
    def atmMain(self,humiditySP,carbonSP,tempatureSP,light):
        if humiditySP is not None:
            if carbonSP is not None:
                if tempatureSP is not None:
                    if light is not None:
                        try:
                            #Output Pin variables
                            L1_Pin = 26 #Light GPIO 25
                            F1_Pin = 6 #Circulation fan GPIO 22
                            F2_Pin = 8 #Exhaust fan GPIO 10
                            F3_Pin = 8 #Electrical exhaust fan GPIO 10
                            F4_Pin = 8 #Electrical intake fan GPIO 10
                            M1_Pin = 25 #Mister GPIO 6

                            #Inputs
                            t1 = run_mode().sensor_Value("T1","C")
                            h1 = run_mode().sensor_Value("H1","%")
                            c1 = run_mode().sensor_Value("C1","%")

                            if run_mode().sensor_Value("F1","") == "ERROR":
                                f1 = 0
                            else:
                                f1 = int(run_mode().sensor_Value("F1",""))

                            if run_mode().sensor_Value("F2","") == "ERROR":
                                f2 = 0
                            else:
                                f2 = int(run_mode().sensor_Value("F2",""))

                            if run_mode().sensor_Value("F3","") == "ERROR":
                                f3 = 0
                            else:
                                f3 = int(run_mode().sensor_Value("F3",""))

                            if run_mode().sensor_Value("F4","") == "ERROR":
                                f4 = 0
                            else:
                                f4 = int(run_mode().sensor_Value("F4",""))

                            if run_mode().sensor_Value("F5","") == "ERROR":
                                f5 = 0
                            else:
                                f5 = int(run_mode().sensor_Value("F5",""))

                            #Processing of inputs
                            temp = t1
                            humid = h1
                            carbon = c1
                            fire = f1 + f2 + f3 + f4 + f5

                            #Output control
                            fireLevel = 10
                            if fire <= fireLevel: #If fire is not detected
                                deviceControl().Light(L1_Pin,light) #Light
                                deviceControl().Fan(F1_Pin, True) #Circulation

                                if tempatureSP <= temp:
                                    deviceControl().Fan(F2_Pin, True) #Exhaust
                                else:
                                    deviceControl().Fan(F2_Pin, False) #Exhaust

                                deviceControl().Mister(M1_Pin, humid, humiditySP) #Mister
                            else:
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
                            return True
                            
                        except Exception as e:
                            errCode = "ERROR COUNTROLING ATMOSPHERE"
                            errMsg = "Error controling atmosphere. The following error code appeared; " + e + "."
                            deviceLog().errorLog(errCode,errMsg)
                            print("ERROR COUNTROLING ATMOSPHERE")
                            return False
                    else:
                        errCode = "NO LIGHT PROVIDED"
                        errMsg = "No light percentage value was provided for the machine."
                        deviceLog().errorLog(errCode,errMsg)
                        print("NO LIGHT PROVIDED")
                        return False
                else:
                    errCode = "NO TEMPATURE SETPOINT PROVIDED"
                    errMsg = "No tempature setpoint value was provided for the machine."
                    deviceLog().errorLog(errCode,errMsg)
                    print("NO TEMPATURE SETPOINT PROVIDED")
                    return False
            else:
                errCode = "NO CARBON SETPOINT PROVIDED"
                errMsg = "No carbon setpoint value was provided for the machine."
                deviceLog().errorLog(errCode,errMsg)
                print("NO CARBON SETPOINT PROVIDED")
                return False
        else:
            errCode = "NO HUMIDITY SETPOINT PROVIDED"
            errMsg = "No humidity setpoint value was provided for the machine."
            deviceLog().errorLog(errCode,errMsg)
            print("NO HUMIDITY SETPOINT PROVIDED")
            return False

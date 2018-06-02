"""
 * @file atmSequence.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified June 2 2018
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
        Output: returns a boolean value to inform the user if the function was compleated or not"""
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
                            F3_Pin = 8 #Intake fan GPIO 10
                            F4_Pin = 8 #Transition fan GPIO 10
                            F5_Pin = 8 #Electrical exhaust fan GPIO 10
                            F6_Pin = 8 #Electrical intake fan GPIO 10
                            M1_Pin = 25 #Mister GPIO 6

                            #Temp sensors
                            t1 = run_mode().sensor_Value("T1","C")

                            #Humidity sensors
                            h1 = run_mode().sensor_Value("H1","%")

                            #Carbon sensors
                            c1 = run_mode().sensor_Value("C1","%")

                            #Fire sensors
                            if run_mode().sensor_Value("F1","") == "ERROR":
                                f1 = 0
                            else:
                                f1 = run_mode().sensor_Value("F1","")
                            if run_mode().sensor_Value("F2","") == "ERROR":
                                f2 = 0
                            else:
                                f2 = run_mode().sensor_Value("F2","")
                            if run_mode().sensor_Value("F3","") == "ERROR":
                                f3 = 0
                            else:
                                f3 = run_mode().sensor_Value("F3","")
                            if run_mode().sensor_Value("F4","") == "ERROR":
                                f4 = 0
                            else:
                                f4 = run_mode().sensor_Value("F4","")
                            if run_mode().sensor_Value("F5","") == "ERROR":
                                f5 = 0
                            else:
                                f5 = run_mode().sensor_Value("F5","")

                            #Processing of inputs
                            temp = int(t1)
                            humid = int(h1)
                            elecTemp = int(t1)
                            carbon = int(c1)
                            fire = int(f1) + int(f2) + int(f3) + int(f4) + int(f5)

                            #Output control
                            fireLevel = 10
                            if fire <= fireLevel: #If fire is not detected
                                deviceControl().Light(L1_Pin,light) #Light
                                deviceControl().Fan(F1_Pin, True) #Circulation

                                if 40 <= elecTemp: #Electrical box to hot
                                    if tempatureSP <= temp: #Too hot
                                        if carbonSP <= carbon: #Too much carbon dioxide
                                            deviceControl().Fan(F2_Pin, True) #Exhaust
                                            deviceControl().Fan(F3_Pin, True) #Intake
                                            deviceControl().Fan(F4_Pin, False) #Transition
                                            deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake
                                        else:
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, True) #Intake
                                            deviceControl().Fan(F4_Pin, True) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake
                                    else:
                                        if carbonSP <= carbon: #Too much carbon dioxide
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, False) #Intake
                                            deviceControl().Fan(F4_Pin, False) #Transition
                                            deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake
                                        else:
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, False) #Intake
                                            deviceControl().Fan(F4_Pin, True) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake
                                else:
                                    if tempatureSP <= temp: #Too hot
                                        if carbonSP <= carbon: #Too much carbon dioxide
                                            deviceControl().Fan(F2_Pin, True) #Exhaust
                                            deviceControl().Fan(F3_Pin, True) #Intake
                                            deviceControl().Fan(F4_Pin, False) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, False) #Electrical intake
                                        else:
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, False) #Intake
                                            deviceControl().Fan(F4_Pin, True) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake
                                    else:
                                        if carbonSP <= carbon: #Too much carbon dioxide
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, False) #Intake
                                            deviceControl().Fan(F4_Pin, False) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, False) #Electrical intake
                                        else:
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, True) #Intake
                                            deviceControl().Fan(F4_Pin, True) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake

                                deviceControl().Mister(M1_Pin, humid, humiditySP) #Mister
                                return True

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
                                return False
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

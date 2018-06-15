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
from logg import deviceLog

class atmosphere():

    """Input: humiditySP - integer value containing the humidity setpoint
              carbonSP - integer value containing the carbon setpoint
              tempatureSP - integer value containing the tempature setpoint in degrees celsius
              light - integer value 0-100 describing the percentage of ligth needed for the day
        Function: controls the atmosphere inside the machine
        Output: returns a boolean value to inform the user if the function was compleated or not"""
    def atmMain(self,humiditySP,carbonSP,tempatureSP,light,elecSP):
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
                            t1 = deviceControl().sensorValue("T1","C")
                            t2 = deviceControl().sensorValue("T2","C")
                            t3 = deviceControl().sensorValue("T3","C")
                            t4 = deviceControl().sensorValue("T4","C")
                            t5 = deviceControl().sensorValue("T5","C")
                            #Weighted average
                            tempBank = [t1,t2,t3,t4,t5]
                            tempWeigth = [1,1,1,1,1]
                            tempCount = 0
                            temp = 0
                            x = 0
                            while x < len(tempBank):
                                if tempBank[x] == "ERROR":
                                    x = x + 1
                                else:
                                    try:
                                        temp = temp + (int(tempBank[x]) * tempWeigth[x])
                                        tempCount = tempCount + 1
                                        x = x + 1
                                    except Exception as e:
                                        x = x + 1
                            if tempCount == 0:
                                temp = "NA"
                                print("SYSTEM FAILURE - TEMPATURE SENSORS OFFLINE")
                            else:
                                temp = temp/tempCount

                            #Humidity sensors
                            h1 = deviceControl().sensorValue("H1","%")
                            h2 = deviceControl().sensorValue("H2","%")
                            h3 = deviceControl().sensorValue("H3","%")
                            h4 = deviceControl().sensorValue("H4","%")
                            h5 = deviceControl().sensorValue("H5","%")
                            humidBank = [h1,h2,h3,h4,h5]
                            humidWeigth = [1,1,1,1,1]
                            humidCount = 0
                            humid = 0
                            x = 0
                            while x < len(humidBank):
                                if humidBank[x] == "ERROR":
                                    x = x + 1
                                else:
                                    try:
                                        humid = humid + (int(humidBank[x]) * humidWeigth[x])
                                        humidCount = humidCount + 1
                                        x = x + 1
                                    except Exception as e:
                                        x = x + 1
                            if humidCount == 0:
                                humid = "NA"
                                print("SYSTEM FAILURE - HUMIDITY SENSORS OFFLINE")
                            else:
                                humid = humid/humidCount

                            #Electrical box sensors
                            t6 = deviceControl().sensorValue("T6","C") #Electrical box
                            h6 = deviceControl().sensorValue("H6","%") #Electrical box
                            try:
                                elecTemp = int(t6)
                            except:
                                elecTemp = "NA"
                                print("SYSTEM FAILURE - ELECTRICAL BOX SENSORS OFFLINE")

                            #Carbon sensors
                            c1 = deviceControl().sensorValue("C1","%")
                            try:
                                carbon = int(c1)
                            except:
                                carbon = "NA"
                                print("SYSTEM FAILURE - CARBON SENSORS OFFLINE")

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
                            if fire <= fireLevel: #If fire is not detected
                                deviceControl().Light(L1_Pin,light) #Light
                                deviceControl().Fan(F1_Pin, True) #Circulation

                                if elecSP <= elecTemp: #Electrical box to hot
                                    if tempatureSP <= temp: #Too hot
                                        if carbonSP <= carbon: #Too much carbon dioxide
                                            deviceControl().Fan(F2_Pin, True) #Exhaust
                                            deviceControl().Fan(F3_Pin, True) #Intake
                                            deviceControl().Fan(F4_Pin, False) #Transition
                                            deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake

                                        elif carbonSP > carbon: #Too little carbon dioxide
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, True) #Intake
                                            deviceControl().Fan(F4_Pin, True) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake

                                        elif carbon == "NA": #Carbon sensors offline
                                            return False

                                    elif tempatureSP > temp: #Too cold
                                        if carbonSP <= carbon: #Too much carbon dioxide
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, False) #Intake
                                            deviceControl().Fan(F4_Pin, False) #Transition
                                            deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake

                                        elif carbonSP > carbon: #Too little carbon dioxide
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, False) #Intake
                                            deviceControl().Fan(F4_Pin, True) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake

                                        elif carbon == "NA": #Carbon sensor offline
                                            return False

                                    elif temp == "NA": #Tempature sensors offline
                                        return False

                                elif elecSP > elecTemp: #Electrical box to cold
                                    if tempatureSP <= temp: #Too hot
                                        if carbonSP <= carbon: #Too much carbon dioxide
                                            deviceControl().Fan(F2_Pin, True) #Exhaust
                                            deviceControl().Fan(F3_Pin, True) #Intake
                                            deviceControl().Fan(F4_Pin, False) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, False) #Electrical intake

                                        elif carbonSP > carbon: #Too little carbon dioxide
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, False) #Intake
                                            deviceControl().Fan(F4_Pin, True) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake

                                        elif carbon == "NA": #Carbon sensor offline
                                            return False

                                    elif tempatureSP > temp: #Too cold
                                        if carbonSP <= carbon: #Too much carbon dioxide
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, False) #Intake
                                            deviceControl().Fan(F4_Pin, False) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, False) #Electrical intake

                                        elif carbonSP > carbon: #Too little carbon dioxide
                                            deviceControl().Fan(F2_Pin, False) #Exhaust
                                            deviceControl().Fan(F3_Pin, True) #Intake
                                            deviceControl().Fan(F4_Pin, True) #Transition
                                            deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                            deviceControl().Fan(F6_Pin, True) #Electrical intake

                                        elif carbon == "NA": #Carbon sensor offline
                                            return False

                                    elif temp == "NA": #Tempature sensors offline
                                        return False

                                elif elecTemp == "NA": #Electical sensors offline
                                    return False

                                deviceControl().Mister(M1_Pin, humid, humiditySP) #Mister
                                return True

                            elif fire > fireLevel:
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

                            elif fire == "NA":
                                return False

                        except Exception as e:
                            errCode = "ERROR CONTROLLING ATMOSPHERE"
                            errMsg = "Error CONTROLLING atmosphere. The following error code appeared; " + str(e) + "."
                            deviceLog().errorLog(errCode,errMsg)
                            print("ERROR CONTROLLING ATMOSPHERE")
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

"""
 * @file atmSequence.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 23 2018
 * @modified August 11 2018
 * @modifiedby BB
 * @brief control sequence for the atmosphere of the machine
 */
 """
from control import deviceControl
from logg import deviceLog
from networking import network

class atmosphere():
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

    """Input: humiditySP - integer value containing the humidity setpoint
              carbonSP - integer value containing the carbon setpoint
              tempatureSP - integer value containing the tempature setpoint in degrees celsius
              light - integer value 0-100 describing the percentage of ligth needed for the day
              elecSP - integer value containing the tempature setpoint in degrees celsius
              ser - open serial instance
        Function: controls the atmosphere inside the machine
        Output: returns a boolean value to inform the user if the function was compleated or not"""
    def atmMain(self,humiditySP,carbonSP,tempatureSP,mainLight,potLight1,potLight2,potLight3,elecSP,ser):
        if humiditySP is not None:
            if carbonSP is not None:
                if tempatureSP is not None:
                    if mainLight is not None:
                        if potLight1 is not None:
                            if potLight2 is not None:
                                if potLight3 is not None:
                                    if elecSP is not None:
                                        if ser is not None:
                                            if ser.isOpen() == True:
                                                #Output Pin variables
                                                L1_Pin = 2 #Light GPIO 8
                                                L2_Pin = 3 #Light GPIO 9
                                                L3_Pin = 4 #Light GPIO 7
                                                L4_Pin = 17 #Light GPIO 0
                                                L5_Pin = 27 #Light GPIO 2
                                                F1_Pin = 22 #Circulation fan GPIO 3
                                                F2_Pin = 10 #Exhaust fan GPIO 12
                                                F3_Pin = 9 #Intake fan GPIO 13
                                                F4_Pin = 11 #Transition fan GPIO 14
                                                F5_Pin = 5 #Electrical exhaust fan GPIO 21
                                                F6_Pin = 6 #Electrical intake fan GPIO 22
                                                M1_Pin = 26 #Mister GPIO 10
                                                sensorBank1 = network.readSerial(ser,1)
                                                sensorBank3 = network.readSerial(ser,3)

                                                #Temp sensors
                                                tBank = deviceControl().sensBank("T","C",5,sensorBank1)
                                                tempWeight = [1,1,1,1,1]
                                                temp = self.wAverage(tBank,tempWeight)
                                                print("temp = " + str(temp))

                                                #Humidity sensors
                                                hBank = deviceControl().sensBank("H","%",5,sensorBank1)
                                                humidWeight = [1,1,1,1,1]
                                                humid = self.wAverage(hBank,humidWeight)
                                                print("humidity = " + str(humid))

                                                #Electrical box sensors
                                                t6 = deviceControl().sensorValue("T6","C",sensorBank1) #Electrical box
                                                h6 = deviceControl().sensorValue("H6","%",sensorBank1) #Electrical box
                                                try:
                                                    elecTemp = int(t6)
                                                    print("Electircal Box Tempature = " + str(elecTemp))
                                                except:
                                                    elecTemp = "NA"
                                                    print("SYSTEM FAILURE - ELECTRICAL BOX SENSORS OFFLINE")

                                                #Carbon sensors
                                                c1 = deviceControl().sensorValue("C1","%",sensorBank1)
                                                try:
                                                    carbon = int(c1)
                                                    print("Carbon contentent = " + str(carbon))
                                                except:
                                                    carbon = "NA"
                                                    print("SYSTEM FAILURE - CARBON SENSORS OFFLINE")

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
                                                fireLevel = 1000
                                                if fire == "NA":
                                                    return False
                                                elif fire <= fireLevel and fire != "NA": #If fire is not detected
                                                    deviceControl().Light(L1_Pin,mainLight) #Light
                                                    deviceControl().Light(L2_Pin,potLight1) #Light
                                                    deviceControl().Light(L3_Pin,potLight2) #Light
                                                    deviceControl().Light(L4_Pin,potLight3) #Light
                                                    deviceControl().Fan(F1_Pin, True) #Circulation

                                                    if elecSP <= elecTemp and elecTemp != "NA": #Electrical box to hot
                                                        if tempatureSP <= temp and temp != "NA": #Too hot
                                                            if carbonSP <= carbon and carbon != "NA": #Too much carbon dioxide
                                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                                deviceControl().Fan(F3_Pin, True) #Intake
                                                                deviceControl().Fan(F4_Pin, False) #Transition
                                                                deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                                print("[f2,f3,f5,f6]")
                                                                print("[1,1,1,1]")

                                                            elif carbonSP > carbon and carbon != "NA": #Too little carbon dioxide
                                                                deviceControl().Fan(F2_Pin, False) #Exhaust
                                                                deviceControl().Fan(F3_Pin, True) #Intake
                                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                                print("[f2,f3,f5,f6]")
                                                                print("[0,1,0,1]")

                                                            elif carbon == "NA": #Carbon sensors offline
                                                                return False

                                                        elif tempatureSP > temp and temp != "NA": #Too cold
                                                            if carbonSP <= carbon and carbon != "NA": #Too much carbon dioxide
                                                                deviceControl().Fan(F2_Pin, False) #Exhaust
                                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                                deviceControl().Fan(F4_Pin, False) #Transition
                                                                deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                                print("[f2,f3,f5,f6]")
                                                                print("[0,0,1,1]")

                                                            elif carbonSP > carbon and carbon != "NA": #Too little carbon dioxide
                                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                                print("[f2,f3,f5,f6]")
                                                                print("[1,0,0,1]")

                                                            elif carbon == "NA": #Carbon sensor offline
                                                                return False

                                                        elif temp == "NA": #Tempature sensors offline
                                                            return False

                                                    elif elecSP > elecTemp and elecTemp != "NA": #Electrical box ok
                                                        if tempatureSP <= temp and temp != "NA": #Too hot
                                                            if carbonSP <= carbon and carbon != "NA": #Too much carbon dioxide
                                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                                deviceControl().Fan(F3_Pin, True) #Intake
                                                                deviceControl().Fan(F4_Pin, False) #Transition
                                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                                deviceControl().Fan(F6_Pin, False) #Electrical intake
                                                                print("[f2,f3,f5,f6]")
                                                                print("[1,1,0,0]")

                                                            elif carbonSP > carbon and carbon != "NA": #Too little carbon dioxide
                                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                                print("[f2,f3,f5,f6]")
                                                                print("[1,0,0,1]")

                                                            elif carbon == "NA": #Carbon sensor offline
                                                                return False

                                                        elif tempatureSP > temp and temp != "NA": #Too cold
                                                            if carbonSP <= carbon: #Too much carbon dioxide
                                                                deviceControl().Fan(F2_Pin, False) #Exhaust
                                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                                deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                                                deviceControl().Fan(F6_Pin, False) #Electrical intake
                                                                print("[f2,f3,f5,f6]")
                                                                print("[0,0,1,0]")

                                                            elif carbonSP > carbon and carbon != "NA": #Too little carbon dioxide
                                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                                print("[f2,f3,f5,f6]")
                                                                print("[1,0,0,1]")

                                                            elif carbon == "NA": #Carbon sensor offline
                                                                return False

                                                        elif temp == "NA": #Tempature sensors offline
                                                            return False

                                                    elif elecTemp == "NA": #Electical sensors offline
                                                        return False

                                                    deviceControl().Mister(M1_Pin, humid, humiditySP) #Mister
                                                    return True

                                                elif fire > fireLevel and fire != "NA":
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
                                            else:
                                                errCode = "SERIAL CLOSED"
                                                errMsg = "The serial instance was closed when provided for the machine."
                                                deviceLog().errorLog(errCode,errMsg)
                                                print("SERIAL CLOSED")
                                                return False
                                        else:
                                            errCode = "NO SERIAL PROVIDED"
                                            errMsg = "No serial instance was provided for the machine."
                                            deviceLog().errorLog(errCode,errMsg)
                                            print("NO SERIAL PROVIDED")
                                            return False
                                    else:
                                        errCode = "NO ELECSP PROVIDED"
                                        errMsg = "No electrical setpoint was provided for the machine."
                                        deviceLog().errorLog(errCode,errMsg)
                                        print("NO ELECSP PROVIDED")
                                        return False
                                else:
                                    errCode = "NO POTLIGHT 3 PROVIDED"
                                    errMsg = "No pot light 3 percentage value was provided for the machine."
                                    deviceLog().errorLog(errCode,errMsg)
                                    print("NO POTLIGHT 3 PROVIDED")
                                    return False
                            else:
                                errCode = "NO POTLIGHT 2 PROVIDED"
                                errMsg = "No pot light 2 percentage value was provided for the machine."
                                deviceLog().errorLog(errCode,errMsg)
                                print("NO POTLIGHT 2 PROVIDED")
                                return False
                        else:
                            errCode = "NO POTLIGHT 1 PROVIDED"
                            errMsg = "No pot light 1 percentage value was provided for the machine."
                            deviceLog().errorLog(errCode,errMsg)
                            print("NO POTLIGHT 1 PROVIDED")
                            return False
                    else:
                        errCode = "NO MAIN LIGHT PROVIDED"
                        errMsg = "No main light percentage value was provided for the machine."
                        deviceLog().errorLog(errCode,errMsg)
                        print("NO MAIN LIGHT PROVIDED")
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

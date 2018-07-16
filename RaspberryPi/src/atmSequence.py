"""
 * @file atmSequence.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 23 2018
 * @modified July 16 2018
 * @modifiedby BB
 * @brief control sequence for the atmosphere of the machine
 */
 """
from runMode import deviceControl
from logg import deviceLog
from networking import network

class atmosphere():
    """Input: valueBank - list containing all values to include in calculation
              weightBank - list containing all weights for the calculation
        Function: determines the weighted average of given values
        Output: returns a real value containing the weighted average"""
    def wAverage(valueBank,weightBank):
        if valueBank is not None:
            if weightBank is not None:
                if len(valueBank) == len(weightBank):
                    count = 0
                    value = 0
                    for x in valueBank:
                        if valueBank[x] != "ERROR":
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
    def atmMain(self,humiditySP,carbonSP,tempatureSP,light,elecSP,ser):
        if humiditySP is not None:
            if carbonSP is not None:
                if tempatureSP is not None:
                    if light is not None:
                        if ser is not None:
                            if ser.is_open() == True:
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
                                sensorBank1 = network().readSerial(ser,1)
                                sensorBank3 = network().readSerial(ser,3)

                                #Temp sensors
                                t1 = deviceControl().sensorValue("T1","C",sensorBank1)
                                t2 = deviceControl().sensorValue("T2","C",sensorBank1)
                                t3 = deviceControl().sensorValue("T3","C",sensorBank1)
                                t4 = deviceControl().sensorValue("T4","C",sensorBank1)
                                t5 = deviceControl().sensorValue("T5","C",sensorBank1)
                                #Weighted average
                                tempBank = [t1,t2,t3,t4,t5]
                                tempWeight = [1,1,1,1,1]
                                temp = self.wAverage(tempBank,tempWeight)
                                print("temp = " + str(temp))

                                #Humidity sensors
                                h1 = deviceControl().sensorValue("H1","%",sensorBank1)
                                h2 = deviceControl().sensorValue("H2","%",sensorBank1)
                                h3 = deviceControl().sensorValue("H3","%",sensorBank1)
                                h4 = deviceControl().sensorValue("H4","%",sensorBank1)
                                h5 = deviceControl().sensorValue("H5","%",sensorBank1)
                                humidBank = [h1,h2,h3,h4,h5]
                                humidWeight = [1,1,1,1,1]
                                humid = self.wAverage(humidBank,humidWeight)
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
                                if deviceControl().sensorValue("F1","",sensorBank3) == "ERROR":
                                    f1 = "NA"
                                else:
                                    f1 = deviceControl().sensorValue("F1","",sensorBank3)
                                if deviceControl().sensorValue("F2","",sensorBank3) == "ERROR":
                                    f2 = "NA"
                                else:
                                    f2 = deviceControl().sensorValue("F2","",sensorBank3)
                                if deviceControl().sensorValue("F3","",sensorBank3) == "ERROR":
                                    f3 = "NA"
                                else:
                                    f3 = deviceControl().sensorValue("F3","",sensorBank3)
                                if deviceControl().sensorValue("F4","",sensorBank3) == "ERROR":
                                    f4 = "NA"
                                else:
                                    f4 = deviceControl().sensorValue("F4","",sensorBank3)
                                if deviceControl().sensorValue("F5","",sensorBank3) == "ERROR":
                                    f5 = "NA"
                                else:
                                    f5 = deviceControl().sensorValue("F5","",sensorBank3)
                                try:
                                    fire = int(f1) + int(f2) + int(f3) + int(f4) + int(f5) #Sum of fire sensors
                                    print("Fire levels are = " + str(fire))
                                except:
                                    fire = "NA"
                                    print("SYSTEM FAILURE - FIRE SENSORS OFFLINE")

                                #Output control
                                fireLevel = 1000
                                if fire == "NA":
                                    return False
                                elif fire <= fireLevel and fire != "NA": #If fire is not detected
                                    deviceControl().Light(L1_Pin,light) #Light
                                    deviceControl().Fan(F1_Pin, True) #Circulation

                                    if elecSP <= elecTemp and elecTemp != "NA": #Electrical box to hot
                                        if tempatureSP <= temp and temp != "NA": #Too hot
                                            if carbonSP <= carbon and carbon != "NA": #Too much carbon dioxide
                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                deviceControl().Fan(F3_Pin, True) #Intake
                                                deviceControl().Fan(F4_Pin, False) #Transition
                                                deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                print("[f2,f3,f4,f5,f6]")
                                                print("[1,1,0,1,1]")

                                            elif carbonSP > carbon and carbon != "NA": #Too little carbon dioxide
                                                deviceControl().Fan(F2_Pin, False) #Exhaust
                                                deviceControl().Fan(F3_Pin, True) #Intake
                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                print("[f2,f3,f4,f5,f6]")
                                                print("[0,1,1,0,1]")

                                            elif carbon == "NA": #Carbon sensors offline
                                                return False

                                        elif tempatureSP > temp and temp != "NA": #Too cold
                                            if carbonSP <= carbon and carbon != "NA": #Too much carbon dioxide
                                                deviceControl().Fan(F2_Pin, False) #Exhaust
                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                deviceControl().Fan(F4_Pin, False) #Transition
                                                deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                print("[f2,f3,f4,f5,f6]")
                                                print("[0,0,0,1,1]")

                                            elif carbonSP > carbon and carbon != "NA": #Too little carbon dioxide
                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                print("[f2,f3,f4,f5,f6]")
                                                print("[1,0,1,0,1]")

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
                                                print("[f2,f3,f4,f5,f6]")
                                                print("[1,1,0,0,0]")

                                            elif carbonSP > carbon and carbon != "NA": #Too little carbon dioxide
                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                print("[f2,f3,f4,f5,f6]")
                                                print("[1,0,1,0,1]")

                                            elif carbon == "NA": #Carbon sensor offline
                                                return False

                                        elif tempatureSP > temp and temp != "NA": #Too cold
                                            if carbonSP <= carbon: #Too much carbon dioxide
                                                deviceControl().Fan(F2_Pin, False) #Exhaust
                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                deviceControl().Fan(F5_Pin, True) #Electrical exhaust
                                                deviceControl().Fan(F6_Pin, False) #Electrical intake
                                                print("[f2,f3,f4,f5,f6]")
                                                print("[0,0,1,1,0]")

                                            elif carbonSP > carbon and carbon != "NA": #Too little carbon dioxide
                                                deviceControl().Fan(F2_Pin, True) #Exhaust
                                                deviceControl().Fan(F3_Pin, False) #Intake
                                                deviceControl().Fan(F4_Pin, True) #Transition
                                                deviceControl().Fan(F5_Pin, False) #Electrical exhaust
                                                deviceControl().Fan(F6_Pin, True) #Electrical intake
                                                print("[f2,f3,f4,f5,f6]")
                                                print("[1,0,1,0,1]")

                                            elif carbon == "NA": #Carbon sensor offline
                                                return False

                                        elif temp == "NA": #Tempature sensors offline
                                            return False

                                    elif elecTemp == "NA": #Electical sensors offline
                                        return False

                                    deviceControl().Mister(M1_Pin, humid, humiditySP) #Mister
                                    return True

                                elif fire > fireLevel and fire != "NA":
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
                            else:
                                errCode = "SERIAL PORT CLOSED"
                                errMsg = "The provided serial port is not open."
                                deviceLog().errorLog(errCode,errMsg)
                                print("SERIAL PORT CLOSED")
                                return False
                        else:
                            errCode = "NO SERIAL PROVIDED"
                            errMsg = "No serial instance was provided for the machine."
                            deviceLog().errorLog(errCode,errMsg)
                            print("NO SERIAL PROVIDED")
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

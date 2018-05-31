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
        #Output Pin variables
        L1_Pin = 26 #Light GPIO 25
        F1_Pin = 6 #Circulation fan GPIO 22
        F2_Pin = 8 #Exhaust fan GPIO 10
        Mister_Pin = 25 #Mister GPIO 6

        #Inputs
        t1 = run_mode().sensor_Value("T1","C")
        h1 = run_mode().sensor_Value("H1","%")
        wl1 = run_mode().sensor_Value("WL1","")
        f1 = run_mode().sensor_Value("F1","")

        #Processing of inputs
        temp = t1
        humid = h1

        #Output control
        deviceControl().Light(L1_Pin,light)
        deviceControl().Fan(F1_Pin, True)

        if tempatureSP <= temp:
            deviceControl().Fan(F2_Pin, True)
        else:
            deviceControl().Fan(F2_Pin, False)

        deviceControl().Mister(Mister_Pin, humid, humiditySP)

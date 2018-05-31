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
    def pumpMain(self):
        #Output Pin variable
        P0_Pin = 9 #Main resevoir pump GPIO 13
        P1_Pin = 5 #Dosing pump GPIO 21
        P2_Pin = 13 #Dosing pump GPIO 23
        P3_Pin = 16 #Dosing pump GPIO 27
        P4_Pin = 1 #Dosing pump GPIO
        P5_Pin = 22 #Dosing pump GPIO 3
        P6_Pin = 27 #Dosing pump GPIO 2
        Drain_Pin =  19 #Drain solenoid GPIO 24

        #Inputs
        wl1 = run_mode().sensor_Value("WL1","")
        f1 = run_mode().sensor_Value("F1","")

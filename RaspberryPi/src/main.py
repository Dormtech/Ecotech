"""
 * @file main.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 21 2018
 * @modified May 23 2018
 * @modifiedby BB
 * @brief main control file for device
 */
 """
from mainGUI import ecozoneApp
#from run_mode import deviceControl

if __name__ == "__main__":
    ecozoneApp().run()

    '''
    #Output Pin variables
    L1_Pin = 26 #Light GPIO 25
    P0_Pin = 9 #Main resevoir pump GPIO 13
    P1_Pin = 5 #Dosing pump GPIO 21
    P2_Pin = 13 #Dosing pump GPIO 23
    P3_Pin = 16 #Dosing pump GPIO 27
    P4_Pin = 1 #Dosing pump GPIO
    P5_Pin = 22 #Dosing pump GPIO 3
    P6_Pin = 27 #Dosing pump GPIO 2
    F1_Pin = 6 #Circulation fan GPIO 22
    F2_Pin = 8 #Exhaust fan GPIO 10
    Drain_Pin =  19 #Drain solenoid GPIO 24
    Mister_Pin = 25 #Mister GPIO 6

    #Setpoints
    Humidity_SP = 60

    #Inputs
    T1 = run_mode().sensor_Value("T1","C")
    H1 = run_mode().sensor_Value("H1","%")
    WL1 = run_mode().sensor_Value("WL1","")
    F1 = run_mode().sensor_Value("F1","")
    Light = 85

    #Processing of inputs
    Temp = T1
    Humid = H1

    #Output control
    run_mode().Light(L1_Pin,Light)
    run_mode().Fan(F1_Pin, True)
    run_mode().Fan(F2_Pin, True)
    run_mode().Mister(Mister_Pin, Humid, Humidity_SP)'''

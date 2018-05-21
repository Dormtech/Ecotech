#*********************************************************************
#Cheech V_01
#Authors:Jake Smiley & Ben Bellerose & Steven Kalapos
#Description: Main control for Ecozone
#*********************************************************************
import os

if __name__ == "__main__":
    updateFile = os.getcwd() + "/cheech.py"
    ip = "192.168.2.38"
    os.system("scp " + updateFile + " pi@" + ip + ":Desktop/Ecozone/Code/RaspberryPi/Control/")

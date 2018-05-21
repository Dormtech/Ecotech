"""
 * @file cheech_upload.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified May 12 2018
 * @modifiedby Ben Bellerose
 * @brief uploads cheech to raspberrypi through SCP protocol
 */
 """
import os

if __name__ == "__main__":
    updateFile = os.getcwd() + "/cheech.py"
    ip = "192.168.2.38"
    os.system("scp " + updateFile + " pi@" + ip + ":Desktop/Ecozone/Code/RaspberryPi/Control/")

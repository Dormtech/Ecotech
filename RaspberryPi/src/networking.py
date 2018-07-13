"""
 * @file networking.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date July 12 2018
 * @modified July 12 2018
 * @modifiedby BB
 * @brief device network interactions
 */
 """
import os
import subprocess
from logg import deviceLog

class network():

    """Input: no input needed for function
        Function: downloads most current version of code avalible
        Output: returns a boolean value to inform user if function was compleated"""
    def machineUpdate(self):
        try:
            if os.path.isdir("/home/pi/Desktop"):
                print("Updating device please wait.")
                os.chdir("/home/pi/Desktop/Ecotech")
                result = subprocess.run(['git','rest','--hard','origin/ben-testBranch'], stdout=subprocess.PIPE)
                result.wait()
                return True
            else:
                print("Downloadign source code please wait.")
                os.chdir("/home/pi/Desktop")
                result = subprocess.run(['git', 'clone', 'https://github.com/Dormtech/Ecotech.git'], stdout=subprocess.PIPE)
                result.wait()
                return True
        except Exception as e:
            errCode = "ERROR UPDATING"
            errMsg = "The following error occured while trying to update: " + str(e)
            deviceLog().errorLog(errCode,errMsg)
            print("ERROR UPDATING")
            return False

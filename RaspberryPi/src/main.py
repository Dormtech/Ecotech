"""
 * @file main.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 21 2018
 * @modified May 30 2018
 * @modifiedby BB
 * @brief main control file for device
 */
 """
from mainGUI import ecozoneApp
#from atmSequence import atmosphere
#from pumpSequence import pumps

if __name__ == "__main__":
    ecozoneApp().run()
    humiditySP = 60
    carbonSP = 10
    tempatureSP = 30
    light = 80
    elecSP = 40
    #atmosphere().atmMain(humiditySP,carbonSP,tempatureSP,light,elecSP)
    #pumps().pumpMain()

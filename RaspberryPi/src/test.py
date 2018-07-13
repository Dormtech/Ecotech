"""
 * @file test.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 26 2018
 * @modified June 25 2018
 * @modifiedby BB
 * @brief testing playground to try out classes
 */
 """
from atmSequence import atmosphere
from pumpSequence import pumps
from networking import network

if __name__ == "__main__":
    humiditySP = 60
    carbonSP = 10
    tempatureSP = 30
    light = 80
    elecSP = 40
    phSP = 50
    #network().machineUpdate()
    atmosphere().atmMain(humiditySP,carbonSP,tempatureSP,light,elecSP)
    pumps().pumpMain(phSP)

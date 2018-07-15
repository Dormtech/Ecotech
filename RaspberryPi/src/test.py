"""
 * @file test.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 26 2018
 * @modified June 25 2018
 * @modifiedby BB
 * @brief testing playground to try out classes
 */
 """
import time
from atmSequence import atmosphere
from pumpSequence import pumps
from networking import network

if __name__ == "__main__":
    startTime = time.time()
    humiditySP = 60
    carbonSP = 10
    tempatureSP = 30
    light = 80
    elecSP = 40
    phSP = 50
    #network().machineUpdate()
    x = 0
    while x < 1:
        print("Count = " + str(x + 1))
        atmosphere().atmMain(humiditySP,carbonSP,tempatureSP,light,elecSP)
        #pumps().pumpMain(phSP)
        print("")
        x = x + 1
    endTime = time.time()
    elapsedTime = endTime - startTime
    print("**********************************")
    print("Start time: " + time.strftime("%H:%M:%S", time.gmtime(start)))
    print("End time: " + time.strftime("%H:%M:%S", time.gmtime(end)))
    print("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(start)))
    print("**********************************")

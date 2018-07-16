"""
 * @file test.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 26 2018
 * @modified July 16 2018
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
    ser = network.openSerial()
    try:
        for x in range(50):
            print("Count = " + str(x + 1))
            atmosphere().atmMain(humiditySP,carbonSP,tempatureSP,light,elecSP,ser)
            #pumps().pumpMain(phSP)
            print("")
        network.closeSerial(ser)
        endTime = time.time()
        elapsedTime = endTime - startTime
        print("**********************************")
        print("Start time: " + time.strftime("%H:%M:%S", time.gmtime(startTime)))
        print("End time: " + time.strftime("%H:%M:%S", time.gmtime(endTime)))
        print("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsedTime)))
        print("**********************************")
    except KeyboardInterrupt or (raw_input().upper() == "END"):
        network.closeSerial(ser)
        endTime = time.time()
        elapsedTime = endTime - startTime
        print("**********************************")
        print("Start time: " + time.strftime("%H:%M:%S", time.gmtime(startTime)))
        print("End time: " + time.strftime("%H:%M:%S", time.gmtime(endTime)))
        print("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsedTime)))
        print("**********************************")

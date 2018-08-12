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
#from atmSequence import atmosphere
#from pumpSequence import pumps
#from networking import network
from logg import deviceLog

if __name__ == "__main__":
    startTime = time.time()
    fullSP = deviceLog().findSP("autoSP.csv",5)
    tempatureSP = fullSP[0]
    humiditySP = fullSP[1]
    carbonSP = fullSP[2]
    mainLight = fullSP[3]
    potLight1 = fullSP[4]
    potLight2 = fullSP[5]
    potLight3 = fullSP[6]
    elecSP = 40
    phSP = 50
    #ser = network.openSerial()

    #Main Loop
    try:
        for x in range(10):
            #print("Count = " + str(x + 1))
            #atmosphere().atmMain(humiditySP,carbonSP,tempatureSP,mainLight,elecSP,ser)
            #pumps().pumpMain(phSP)
            print("")
        #network.closeSerial(ser)
        endTime = time.time()
        elapsedTime = endTime - startTime
        print("**********************************")
        print("Start time: " + time.strftime("%H:%M:%S", time.gmtime(startTime)))
        print("End time: " + time.strftime("%H:%M:%S", time.gmtime(endTime)))
        print("Elapsed time: " + str(elapsedTime))
        print("**********************************")
    except KeyboardInterrupt or (raw_input().upper() == "END"):
        #network.closeSerial(ser)
        endTime = time.time()
        elapsedTime = endTime - startTime
        print("**********************************")
        print("Start time: " + time.strftime("%H:%M:%S", time.gmtime(startTime)))
        print("End time: " + time.strftime("%H:%M:%S", time.gmtime(endTime)))
        print("Elapsed time: " + str(elapsedTime))
        print("**********************************")

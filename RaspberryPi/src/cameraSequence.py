"""
 * @file cameraSequence.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date June 2018
 * @modified June 20 2018
 * @modifiedby BB
 * @brief control sequence for the camera of the machine
 */
 """

import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

class camera():

    """Input: fileName - string value containing the name you wish to save photo as
        Function: takes and saves picture of plant
        Output: returns a boolean value to inform user of machine state"""
    def cameraMain(fileName):
        if fileName is not None:
            cameraPi = PiCamera()
            rawCapture = PiRGBArray(cameraPi)
            time.sleep(0.1)
            cameraPi.capture(rawCapture, format="bgr")
            image = rawCapture.array
            cv2.imwrite(fileName,image)
            cameraPi.close()
            #cv2.imshow("Image", image)
            #cv2.waitKey(0)
            return True
        else:
            errCode = "NO FILE NAME PROVIDED"
            errMsg = "No file name was provided for the photo to be saved as."
            deviceLog().errorLog(errCode,errMsg)
            print("NO FILE NAME PROVIDED")
            return False

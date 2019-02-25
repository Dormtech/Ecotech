"""
 * @file logg.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified Feb 22 2019
 * @modifiedby Sk
 * @brief logging systems for device
 */
 """
import os
import csv
import shutil
import datetime
from time import gmtime,strftime
import pandas as pd

class plant_csv():

    def __init__(self):
        super(create_CSV, self).__init__(**kwargs)

        """Input: strain - name of strain of the plant
                  plantNmae - name of plant trying to be created
            Function: creates csv log for a new plant
            Output: True if sucessful; else false"""
    def create_CSV(strain, plantName):
        if plant_csv.doesExist(plantName) == True:
            return False

        plantDays = 20
        newPlantFile = pd.DataFrame({"Day":pd.Series(range(plantDays)),
        "Strain": strain,
        "Name": plantName,
        "Done": 'F'})

        if os.name == 'posix':
            newPlantFile.to_csv('files/PlantFiles/%s.csv'%plantName)
        else:
            newPlantFile.to_csv("files\PlantFiles\%s.csv"%plantName)

        plant_csv.add_plant(plantName)
        return True

    """Input:plantName - name of plant trying to be added
        Function: adds plant to the beginning of the plant list (displayed first in contnue)
        Output: NULL"""
    def add_plant(plantName):
        if os.name == 'posix':
            fp = open("files/GuiFiles/plants.txt", mode='r+')
            fp.write(plantName+'\n')
            fp.close()
        else:
            fp = open("files\GuiFiles\plants.txt", mode='r+')
            fp.write(plantName+'\n')
            fp.close()
        return
       
    """Input:plantName - name of plant trying to be created
    Function: checks if plat has already been created before
    Output: True if it exist; flase if it doesnt"""
    def doesExist(plantName):
        if os.name == 'posix':
            check = os.path.isfile('files/PlantFiles/%s.csv'%plantName)
        else:
            check = os.path.isfile('files\PlantFiles\%s.csv'%plantName)
        return check

class strain_csv():
    """docstring for strain_csv.
    holds all the functions to read strain documents"""
    def __init__(self, arg):
        super(strain_csv, self).__init__()
        self.arg = arg

    def getStrain():
        pass

class deviceLog():

    def __init__(self):
        dirHold = os.getcwd().split("/")
        dirHold = dirHold[:-1]
        self.logDir = "/".join(dirHold) + str("/logs/")

    """Input: type - string containing error code relarted to error type
              description - string containing description of what caused error
        Function: logs what vaused the error in desired location
        Output: returns a boolean value to inform user of log state"""
    def errorLog(self,errorType,description):
        if errorType is not None:
            if description is not None:
                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                content = str(date) + ":" + str(errorType) + ": " + str(description)
                #set location of log file
                logFile = str(self.logDir) + str("errorLog.txt")
                #check if path is already there
                if self.writeFile(logFile,content) == True:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    """Input: index = integer conatining current index of the plant cycle
              name = string containing name specific for the current plant
              strain = string containing current strain of the plant
              stats = list containing current machine statistics
        Function: logs daily machine stats for further processing
        Output: writes boolean value to show user success of the process"""
    def dayLog(self,index,name,strain,stats):
        if index is not None:
            if name is not None:
                if strain is not None:
                    if stats is not None:
                        #variables
                        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        logFile = str(self.logDir) + str("dayLog.txt")
                        content = [str(date),"Index=" + str(index),"Name=" + str(name),"Strain=" + str(strain)]
                        for x in range(len(stats)):
                            content.insert(len(content),stats[x])
                        content = "~".join(content)
                        if self.writeFile(logFile,content) == True:
                            return True
                        else:
                            errCode = "FAILED TO WRITE"
                            errMsg = "Unable to write to desired file."
                            self.errorLog(errCode,errMsg)
                            print("FAILED TO WRITE")
                            return False
                    else:
                        errCode = "NO STATS GIVEN"
                        errMsg = "No machine statistics were given to the function."
                        self.errorLog(errCode,errMsg)
                        print("NO STATS GIVEN")
                        return False
                else:
                    errCode = "NO STRAIN GIVEN"
                    errMsg = "No strain was given to the function."
                    self.errorLog(errCode,errMsg)
                    print("NO STRAIN GIVEN")
                    return False
            else:
                errCode = "NO NAME GIVEN"
                errMsg = "No plant name was given to the function."
                self.errorLog(errCode,errMsg)
                print("NO NAME GIVEN")
                return False

        else:
            errCode = "NO INDEX GIVEN"
            errMsg = "No index was given to the function."
            self.errorLog(errCode,errMsg)
            print("NO INDEX GIVEN")
            return False

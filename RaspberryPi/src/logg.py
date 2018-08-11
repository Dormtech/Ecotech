"""
 * @file logg.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified July 20 2018
 * @modifiedby BB
 * @brief logging systems for device
 */
 """
import os
import csv
import shutil
from time import gmtime,strftime

class deviceLog():

    def __init__(self):
        dirHold = os.getcwd().split("/")
        del dirHold[:1]
        print(dirHold)
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
                #attempt to read log file
                if os.path.isfile(logFile):
                    fileRead = open(logFile,"r")
                    #write error log into existing error log
                    fileHold = fileRead.readlines()
                    fileRead.close()
                    fileHold.insert(len(fileHold),content)
                    fileWrite = open(logFile,"w")
                    x = 0
                    while x < len(fileHold):
                        fileWrite.write(fileHold[x].replace("\n",""))
                        if x < len(fileHold) - 1:
                            fileWrite.write("\n")
                        x = x + 1
                    fileWrite.close()
                    return True
                else:
                    fileWrite = open(logFile,"w+")
                    fileWrite.write(content)
                    fileWrite.close()
                    return True
            else:
                return False
        else:
            return False

    """Input: fileName - string containing file adress to csv file
        Function: reads CSV file and return the contents
        Output: returns a list containing the values for the setpoints and their values"""
    def readCSV(self,fileName):
        if fileName is not None:
            fullFile = str(self.logDir) + str(fileName)
            if os.path.isfile(fullFile):
                try:
                    fileOpen = open(fullFile, "r")
                    content = list(csv.reader(fileOpen))
                    return content
                except Exception as e:
                    errCode = "ERROR READING FILE"
                    errMsg = "Error reading CSV file. The following error code appeared; " + str(e)
                    self.errorLog(errCode,errMsg)
                    print("ERROR READING FILE")
                    content = None
                    return content
            else:
                errCode = "FILE NOT FOUND"
                errMsg = "The given file adress for the CSV file does not exist."
                self.errorLog(errCode,errMsg)
                print("FILE NOT FOUND")
                content = None
                return content
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "No file name was given for the CSV file."
            self.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
            content = None
            return content

    """Input: content - list containing data you want to input into csv
              fileName - string containing the name of the file
       Function: overwrite all data inside of the csv with chosen data
       Output: writes boolean value to show user success of csv write"""
    def inputCSV(self,content,fileName):
        if content is not None:
            if fileName is not None:
                fullFile = str(self.logDir) + str(fileName)
                if os.path.isfile(fullFile):
                    try:
                        with open(fullFile, 'wb') as csvfile:
                            spamWriter = csv.writer(csvfile, delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)
                            for x in range(len(content)):
                                rowHold = []
                                for a in range(len(content[x])):
                                    rowHold.insert(len(rowHold),content[x][a])
                                spamWriter.writerow(rowHold)
                        return True
                    except Exception as e:
                        errCode = "ERROR WRITING CSV"
                        errMsg = "Unable to write the CSV file. The following error occured; " + str(e)
                        self.errorLog(errCode,errMsg)
                        print("ERROR WRITING CSV")
                        return False
                else:
                    errCode = "FILE NOT FOUND"
                    errMsg = "The given file adress for the CSV file does not exist."
                    self.errorLog(errCode,errMsg)
                    print("FILE NOT FOUND")
                    return False
            else:
                errCode = "NO FILE GIVEN"
                errMsg = "A file adress was not given as an input."
                self.errorLog(errCode,errMsg)
                print("NO FILE GIVEN")
                return False
        else:
            errCode = "NO CONTENT GIVEN"
            errMsg = "There was no content given as an input."
            self.errorLog(errCode,errMsg)
            print("NO CONTENT GIVEN")
            return False

    """Input: fileName - string containing the name of the file you wish to duplicate
              newName - string containing the name of the resultant file
       Function: duplicates a file and renames it to a name of your choice.
       Output: writes boolean value to show user success of csv write"""
    def duplicateFile(fileName,newName):
        if fileName is not None:
            if newName is not None:
                if os.path.isfile(newName):
                    os.remove(newName)
                    time.sleep(0.1)
                if os.path.isfile(fileName):
                    shutil.copyfile(fileName,newName)
                    return True
                else:
                    errCode = "FILE NOT FOUND"
                    errMsg = "The given file could not be found."
                    self.errorLog(errCode,errMsg)
                    print("FILE NOT FOUND")
                    return False
            else:
                errCode = "NO NEW NAME GIVEN"
                errMsg = "There was no new file name given as an input."
                self.errorLog(errCode,errMsg)
                print("NO NEW NAME GIVEN")
                return False
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "There was no file name as an input."
            self.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
            return False

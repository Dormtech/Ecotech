"""
 * @file filer.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date January 5 2019
 * @modified January 5 2019
 * @modifiedby BB
 * @brief class dedicated to file management within the machine
 */
 """
import os
import csv
from logger import deviceLog

class filer():

    """Input: fileName - string containing file adress
       Function: determines the file extension of a file adress
       Output: returns a string containing the file type"""
    def fileType(self,fileName):
        if fileName == '':
            return False
        else:
            extensions = ['csv']
            check = False
            for ext in extensions:
                if fileName.lower().endswith(ext):
                    return ext

    """Input: fileName - string containing file adress to csv file
              content - string you wish to write in file
        Function: stores contents in text file for later retreval.
        Output: writes boolean value to show user success of the process"""
    def writeFile(self,fileName,content):
        if fileName is not None:
            if content is not None:
                #check if path is already there
                if os.path.isfile(fileName):
                    fileRead = open(fileName,"r")
                    fileHold = fileRead.readlines()
                    fileRead.close()
                    fileHold.insert(len(fileHold),content)
                    fileWrite = open(fileName,"w")
                    for x in range(len(fileHold)):
                        fileWrite.write(fileHold[x].replace("\n",""))
                        if x < len(fileHold) - 1:
                            fileWrite.write("\n")
                    fileWrite.close()
                    return True
                else:
                    fileWrite = open(fileName,"w+")
                    fileWrite.write(content)
                    fileWrite.close()
                    return True
            else:
                errCode = "NO CONTENT GIVEN"
                errMsg = "No content was given for the file to write."
                deviceLog.errorLog(errCode,errMsg)
                print("NO CONTENT GIVEN")
                return False
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "No file name was given for the file."
            deviceLog.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
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
                    deviceLog.errorLog(errCode,errMsg)
                    print("ERROR READING FILE")
                    content = None
                    return content
            else:
                errCode = "FILE NOT FOUND"
                errMsg = "The given file adress for the CSV file does not exist."
                deviceLog.errorLog(errCode,errMsg)
                print("FILE NOT FOUND")
                content = None
                return content
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "No file name was given for the CSV file."
            deviceLog.errorLog(errCode,errMsg)
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
                        deviceLog.errorLog(errCode,errMsg)
                        print("ERROR WRITING CSV")
                        return False
                else:
                    errCode = "FILE NOT FOUND"
                    errMsg = "The given file adress for the CSV file does not exist."
                    deviceLog.errorLog(errCode,errMsg)
                    print("FILE NOT FOUND")
                    return False
            else:
                errCode = "NO FILE GIVEN"
                errMsg = "A file adress was not given as an input."
                deviceLog.errorLog(errCode,errMsg)
                print("NO FILE GIVEN")
                return False
        else:
            errCode = "NO CONTENT GIVEN"
            errMsg = "There was no content given as an input."
            deviceLog.errorLog(errCode,errMsg)
            print("NO CONTENT GIVEN")
            return False

    """Input: fileName - string containing file adress to csv file
              name = string containing name specific for the current plant
        Function: determines current index of plant cycle
        Output: writes integer value containing current index"""
    def findIndex(self,fileName,name):
        if fileName is not None:
            fullFile = str(self.logDir) + str(fileName)
            if os.path.isfile(fullFile):
                #Read file
                fileRead = open(fullFile,"r")
                fileHold = fileRead.readlines()
                fileRead.close()

                #Find most recent day log
                for x in range(len(fileHold)):
                    recentLog = fileHold[len(fileHold)-(x+1)].split("~")
                    logDate = recentLog[0].split(" ")[0]
                    logName = recentLog[2].split("=")[1].strip()
                    if str(name) == str(logName):
                        break

                #Determine index of day
                if str(name) == str(logName):
                    if logDate == strftime("%Y-%m-%d", gmtime()):
                        index = int(recentLog[1].split("=")[1])
                        return index
                    else:
                        logDate = datetime.date(int(logDate.split("-")[0]),int(logDate.split("-")[1]),int(logDate.split("-")[2]))
                        diff = datetime.date.today() - logDate
                        if int(recentLog[1].split("=")[1]) + int(diff.days) < len(self.readCSV("autoSP.csv")):
                            index = int(recentLog[1].split("=")[1]) + int(diff.days)
                        else:
                            index = 0
                        return index
                else:
                    index = 0
                    return index
            else:
                index = 0
                return index
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "No file name was given for the file."
            deviceLog.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
            return "NA"

    """Input: fileName - string containing the name of the file you wish to search
              index - integer containing the current day of the schedule
       Function: gathers all setpoints for a given index.
       Output: writes list containing all setpoints for the given index"""
    def findSP(self,fileName,index):
        if fileName is not None:
            if index is not None:
                if type(index) == int:
                    #Variables
                    fullSchedule = self.readCSV(fileName)
                    fullSP = fullSchedule[int(index)+2]
                    tempBank = [fullSP[1],fullSP[2],fullSP[3]]
                    humidBank = [fullSP[4],fullSP[5],fullSP[6]]
                    CO2Bank = [fullSP[7],fullSP[8],fullSP[9]]
                    lightBank = [fullSP[10],fullSP[11],fullSP[12],fullSP[13]]
                    curTime = strftime("%H", gmtime())

                    #Determine setpoints based on day time
                    if int(curTime) <= 8:
                        setpoints = [tempBank[0],humidBank[0],CO2Bank[0]]
                    elif int(curTime) > 8 and int(curTime) <= 16:
                        setpoints = [tempBank[1],humidBank[1],CO2Bank[1]]
                    elif int(curTime) > 16 and int(curTime) <= 24:
                        setpoints = [tempBank[2],humidBank[2],CO2Bank[2]]
                    for x in range(len(lightBank)):
                        setpoints.insert(len(setpoints),lightBank[x])
                    return setpoints
                else:
                    errCode = "INDEX NOT INTEGER"
                    errMsg = "The given index was not the correct data type."
                    deviceLog.errorLog(errCode,errMsg)
                    print("INDEX NOT INTEGER")
                    return ["ERROR"]
            else:
                errCode = "NO INDEX GIVEN"
                errMsg = "There was no index provided as an input."
                deviceLog.errorLog(errCode,errMsg)
                print("NO INDEX GIVEN")
                return ["ERROR"]
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "There was no file name as an input."
            deviceLog.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
            return ["ERROR"]

    """Input: fileName - string containing the name of the file you wish to duplicate
              newName - string containing the name of the resultant file
       Function: duplicates a file and renames it to a name of your choice.
       Output: writes boolean value to show user success of csv write"""
    def duplicateFile(self,fileName,newName):
        if fileName is not None:
            if newName is not None:
                fullFile = str(self.logDir) + str(fileName)
                fullNew = str(self.logDir) + str(newName)
                if os.path.isfile(fullNew):
                    os.remove(newName)
                    time.sleep(0.1)
                if os.path.isfile(fullFile):
                    shutil.copyfile(fullFile,fullNew)
                    return True
                else:
                    errCode = "FILE NOT FOUND"
                    errMsg = "The given file could not be found."
                    deviceLog.errorLog(errCode,errMsg)
                    print("FILE NOT FOUND")
                    return False
            else:
                errCode = "NO NEW NAME GIVEN"
                errMsg = "There was no new file name provided as an input."
                deviceLog.errorLog(errCode,errMsg)
                print("NO NEW NAME GIVEN")
                return False
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "There was no file name provided as an input."
            deviceLog.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
            return False

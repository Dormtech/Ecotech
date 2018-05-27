"""
 * @file logging.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
<<<<<<< HEAD
 * @modified May 21 2018
=======
 * @modified May 27 2018
>>>>>>> testbranch
 * @modifiedby BB
 * @brief logging systems for device
 */
 """
import os
from time import gmtime,strftime

class deviceLog():

    """Input: type - String containing error code relarted to error type
              description - String containing description of what caused error
        Function: logs what vaused the error in desired location
        Output: returns a boolean value to inform user of log state"""
    def errorLog(self,errorType,description):
        if errorType is not None:
            if description is not None:
                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                content = str(date) + "-" + str(errorType) + ": " + str(description)
<<<<<<< HEAD
                log_file = os.getcwd() + "/error_log.txt"
                try:
                    file_read = open(log_file,"r")
                except Exception as e:
                    file_write = open(log_file,"w")
                    file_write.write(content)
                    return True
=======
                #set location of log file
                log_file = os.getcwd().split("/")
                del log_file[len(log_file) - 1]
                log_file = "/".join(log_file)
                log_file = log_file + "/logs/error_log.txt"
                #attempt to read log file
                try:
                    file_read = open(log_file,"r")
                except Exception as e:
                    #unable to find error log creating new error log
                    file_write = open(log_file,"w")
                    file_write.write(content)
                    return True
                #write error log into existing error log
>>>>>>> testbranch
                file_hold = file_read.readlines()
                file_read.close()
                file_hold.insert(len(file_hold),content)
                file_write = open(log_file,"w")
                x = 0
                while x < len(file_hold):
                    file_write.write(file_hold[x].replace("\n",""))
                    if x < len(file_hold) - 1:
                        file_write.write("\n")
                    x = x + 1
                return True
            else:
                return False
        else:
            return False

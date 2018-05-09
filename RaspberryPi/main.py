#**********************************************************************************
#Main V0_01
#Authors: Jake Smiley & Ben Bellerose
#Description: This is the main control for the Ecozone box.
#**********************************************************************************
import os
import sys
import time
import shutil
import subprocess

def DeviceControl(Homedir):
    os.chdir(Homedir)
    os.chdir("Control")
    p = subprocess.Popen(["python","cheech.py"], shell=False)
    return p

def UserInterface(Homedir):
    try:
        #Check for current running process and kills all on port 5000
        port = subprocess.check_output(['lsof','-i:5000'])
        port = port.split(" ")
        x = 0
        a = 0
        cur_proc = []
        while x < len(port):
            if len(port[x]) > 1:
                a = a + 1
                if a == 1:
                    cur_proc.insert(len(cur_proc),port[x])
                elif a == 9:
                    a = 0
            x = x + 1
        del cur_proc[0]
        cur_proc = list(set(cur_proc))
        x = 0
        while x < len(cur_proc):
            os.system("kill " + cur_proc[x])
            x = x + 1
    except:
        pass

    #Run server for users to interact with
    os.chdir(Homedir)
    os.chdir("UI")
    p = subprocess.Popen(["python","app.py"], shell=False) #To turn off webserver run program with this process commented out
    return p

if __name__=='__main__':
    Homedir = os.getcwd()
    print("**********************************")
    print("Starting up machine...")
    UI = UserInterface(Homedir)
    DC = DeviceControl(Homedir)
    while True:
        print("Type 'END' to shut program down...")
        print("**********************************")
        command = raw_input()
        if command.upper() == "END":
            print("**********************************")
            print("Shutting down machine...")
            UI.terminate()
            try:
                UI.kill()
                UI.wait()
                if int(UI.returncode) < 0:
                    print("Process killed")
            except:
                if int(UI.returncode) < 0:
                    print("Process terminated")
            DC.terminate()
            try:
                DC.kill()
                DC.wait()
                if int(UI.returncode) < 0:
                    print("Process killed")
            except:
                if int(UI.returncode) < 0:
                    print("Process terminated")        
            #make duplicate of app file to kill app child processes
            shutil.copyfile(Homedir + "/UI/app.py", Homedir + "/UI/app1.py")
            os.remove(Homedir + "/UI/app.py")
            os.rename(Homedir + "/UI/app1.py", Homedir + "/UI/app.py")
            time.sleep(2)
            print("Goodbye...")
            print("**********************************")
            sys.exit()

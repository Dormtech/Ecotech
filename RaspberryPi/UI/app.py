#**********************************************************************************
#App 0_01
#Authors: Jake Smiley & Ben Bellerose
#Description: This is the routing for the user controled web app///
#**********************************************************************************
from flask import Flask, render_template, request, redirect, session
from time import gmtime, strftime
from passlib.hash import sha256_crypt
import os
import csv

app = Flask(__name__)
app.secret_key = 'Aswe23f#ts4!63fsFARE@!'

#Reads values from a csv file
def read_csv(CSV_File):
    External_txt = ''
    External_txt = open(CSV_File, "r")
    External_txt = csv.reader(External_txt)
    External_txt = list(External_txt)
    return External_txt

def XYfind(content,value):
    x = 0
    data = ""
    while x < len(content):
        a = 0
        while a < len(content[x]):
            if str(content[x][a]) == str(value):
                data = content[x]
                a = len(content[x])
            else:
                a = a + 1
        if len(data) > 0:
            x = len(content)
        else:
            x = x + 1
    return data

#Writes to csv file
def input_csv(Content, CSV_File):
    if len(Content) >= 1:
        with open(CSV_File, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)
            x = 0
            while x < len(Content):
                a = 0
                Hold = []
                while a < len(Content[x]):
                    Hold.insert(len(Hold),Content[x][a])
                    a = a + 1
                spamwriter.writerow(Hold)
                x = x + 1
        return("Input Complete")
    else:
        return("Error With Input")

#Find location of main folder
def Homedir():
    Homedir = os.getcwd() + "/"
    Homedir = Homedir.split("/")
    del Homedir[len(Homedir)-1]
    del Homedir[len(Homedir)-1]
    Homedir = "/".join(Homedir)
    Homedir = Homedir + "/"
    return Homedir

@app.route("/")
def index():
    values = read_csv(Homedir() + "Control/control_files/current_values.csv")
    power_var = values[1][0]
    if  power_var == "0":
        _Power = "OFF"
    elif power_var == "1":
        _Power = "ON"
    _Date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    _Temp = values[1][3] + " C"
    _TempSetpoint = values[1][5] + " C"
    _Humid = values[1][4] + " %"
    _HumidSetpoint = values[1][6] + " %"
    _Cycle = values[1][8] + " Days"
    _Index = int(values[1][1]) + 1
    _Plant = "NA"
    _PH = "NA"
    _PHsetpoint = "NA"
    _Light = "NA"
    if session.get('user'):
        Log = "Log Out"
    else:
        Log = ""
    return render_template('autocontrol.html',power=_Power,date=_Date,temp=_Temp,humid=_Humid,cycle=_Cycle,tempsetpoint=_TempSetpoint,humidsetpoint=_HumidSetpoint,plant=_Plant,index=_Index,user=Log,ph=_PH,light=_Light,phsetpoint=_PHsetpoint)

@app.route("/PowerOn/<Hold>")
def PowerOn(Hold):
    if session.get('user'):
        Verify = read_csv(Homedir() + "Control/control_files/current_values.csv")
        x = 0
        while Verify[0] != "1" and x < 5000:
            Verify = read_csv(Homedir() + "Control/control_files/current_values.csv")
            x = x + 1
        if Hold == "M":
            Control = open(Homedir() + "Control/control_files/power_control.txt", "w")
            Control.write("1-0")
            Control.close()
            return redirect('/ManualControl')
        elif Hold == "A":
            Control = open(Homedir() + "Control/control_files/power_control.txt", "w")
            Control.write("1-1")
            Control.close()
            return redirect('/')
    else:
        return redirect('/UserLogin/'+ Hold)

@app.route("/PowerOff/<Hold>")
def PowerOff(Hold):
    if session.get('user'):
        Verify = read_csv(Homedir() + "Control/control_files/current_values.csv")
        x = 0
        while Verify[0] != "0" and x < 5000:
            Verify = read_csv(Homedir() + "Control/control_files/current_values.csv")
            x = x + 1
        if Hold == "M":
            Control = open(Homedir() + "Control/control_files/power_control.txt", "w")
            Control.write("0-0")
            Control.close()
            return redirect('/ManualControl')
        elif Hold == "A":
            Control = open(Homedir() + "Control/control_files/power_control.txt", "w")
            Control.write("0-1")
            Control.close()
            return redirect('/')
    else:
        return redirect('/UserLogin/'+ Hold)

@app.route("/UserLogin/<Hold>")
def UserLogin(Hold):
    return render_template('login.html',hold=Hold)

@app.route("/LoginVerification/<Hold>",methods=['POST'])
def LoginVerification(Hold):
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    try:
        user_list = read_csv(Homedir() + "/UI/datafiles/users.csv")
        user = XYfind(user_list,_email)
        if sha256_crypt.verify(_password, user[2]) == True:
            session['user'] = _email
            if Hold == "M":
                return redirect('/ManualControl')
            elif Hold == "A":
                return redirect('/')
        else:
            return redirect('/UserLogin/'+ Hold)
    except:
        return redirect('/UserLogin/'+ Hold)

@app.route("/LogOut")
def LogOut():
    session.pop('user',None)
    return redirect('/')

@app.route("/UserSignUp/<Hold>")
def UserSignUp(Hold):
    return render_template('signup.html', hold=Hold)

@app.route("/SignUpVerification/<Hold>",methods=['POST'])
def SignUpVerification(Hold):
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = sha256_crypt.encrypt(request.form['inputPassword'])
    _Date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    Users = read_csv(Homedir() + "/UI/datafiles/users.csv")
    newUser = [_name,_email,_password,_Date]
    x = 0
    usercheck = ""
    while x < len(newUser):
        usercheck = XYfind(Users,str(newUser[x]))
        if len(usercheck) > 0:
            x = len(newUser)
        x = x + 1
    Users.insert(len(Users),newUser)
    if usercheck == "":
        input_csv(Users,Homedir() + "/UI/datafiles/users.csv")
        session['user'] = _email
        if Hold == "M":
            return redirect('/ManualControl')
        elif Hold == "A":
            return redirect('/')
    else:
        return redirect('/UserSignUp/'+ Hold)

@app.route("/ManualControl")
def ManualControl():
    if session.get('user'):
        values = read_csv(Homedir() + "Control/control_files/current_values.csv")
        power_var = values[1][0]
        if  power_var == "0":
            _Power = "OFF"
        elif power_var == "1":
            _Power = "ON"
        _Date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        _Temp = values[1][2] + " C"
        _TempSetpoint = values[1][4] + " C"
        _Humid = values[1][3] + " %"
        _HumidSetpoint = values[1][5] + " %"
        _Cycle = values[1][7] + " Days"
        _Index = int(values[1][0]) + 1
        _Plant = "NA"
        _PH = "NA"
        _PHsetpoint = "NA"
        _Light = "NA"
        Log = "Log Out"
        return render_template('manualcontrol.html',power=_Power,date=_Date,temp=_Temp,humid=_Humid,cycle=_Cycle,tempsetpoint=_TempSetpoint,humidsetpoint=_HumidSetpoint,plant=_Plant,index=_Index,user=Log,ph=_PH,light=_Light,phsetpoint=_PHsetpoint)
    else:
        return redirect('/UserLogin/M')

@app.route("/UpdateSettings",methods=['POST'])
def UpdateSettings():
    return redirect("/ManualControl")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

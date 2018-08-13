"""
 * @file mainGUI.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 22 2018
 * @modified August 13 2018
 * @modifiedby BB
 * @brief GUI managment and creation
 */
 """
import kivy
from cameraSequence import camera
from atmSequence import atmosphere
from control import deviceControl
from networking import network
from logg import deviceLog

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.graph import MeshLinePlot

import random, os, time

from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

global buttonPressed

class GUIFunc():

    #creates the option file used to store user config
    def createGUIOptions(pathway):
        optionFile = open(pathway+"/options/GUIOptions.txt","w+")
        return optionFile

#default stats display
class defaultScreen(Screen):

    def __init__(self, **kwargs):
        super(defaultScreen, self).__init__(**kwargs)

        pathway = os.path.dirname(os.path.abspath( __file__ ))
        try:
            optionFile = open(pathway+"/options/GUIOptions.txt","r+")
        except IOError:
            optionFile = createGUIOptions(pathway)

        self.addWidgetsDefault(optionFile)
        Clock.schedule_interval(self.update, 1)
        self.ser = network.openSerial()
        self.plantName = "Plant1"
        self.plantStrain = "Kush"
        deviceLog().dayLog(deviceLog().findIndex("dayLog.txt","Machine Start"),"Machine Start","NA")

    #will update all the variables on screen
    def update(self, dt):
        sensorBank1 = network.readSerial(self.ser,1)
        temp = self.updateTemp(sensorBank1)
        humid = self.updateHumid(sensorBank1)
        CO2 = self.updateCO2(sensorBank1)
        day = self.updateIndex(self.plantName)
        self.temperatureVar.text = str(temp)
        self.humidityVar.text = str(humid)
        self.CO2Var.text = str(CO2)
        self.strainVar.text = 'NA'
        self.dayVar.text = str(day)
        self.clockDisplay.text = time.asctime()

    #updates temperature
    def updateTemp(self,sensorBank):
        tBank = deviceControl().sensBank("T","C",5,sensorBank)
        tempWeight = [1,1,1,1,1]
        return atmosphere().wAverage(tBank,tempWeight)

    #updates humidity
    def updateHumid(self,sensorBank):
        hBank = deviceControl().sensBank("H","%",5,sensorBank)
        humidWeight = [1,1,1,1,1]
        return atmosphere().wAverage(hBank,humidWeight)

    #updates the index
    def updateIndex(self,plantName):
        index = deviceLog().findIndex("dayLog.txt",plantName)
        return index

    #update CO2
    def updateCO2(self,sensorBank):
        c1 = deviceControl().sensorValue("C1","%",sensorBank)
        return c1

    def takePicture(self,plantName,plantStrain):
        try:
            index = deviceLog().findIndex("dayLog.txt",plantName)
            deviceLog().dayLog(index,plantName,plantStrain)
            dirHold = os.getcwd().split("/")
            dirHold = dirHold[:-1]
            picDir = "/".join(dirHold) + str("logs/pics")
            if os.path.isdir(picDir) == False:
                os.mkdir(picDir)
            fileName = picDir + "/" + plantName + "(" + time.strftime("%d-%y-%m_%H:%M:%S", time.gmtime()) + ").png"
            if os.path.isfile(fileName):
                os.remove(fileName)
                time.sleep(0.1)
                self.remove_widget(self.imgVar)
            control.takePicture(fileName)
            self.imgVar = Image(source=fileName, pos=(200,75), size_hint=(.5,.5))
            self.add_widget(self.imgVar)
        except Exception as e:
            errCode = "FAILED TO TAKE PICTURE"
            errMsg = "Failed while attempting to take picture with the following error " + str(e)
            deviceLog().errorLog(errCode,errMsg)

    #reads the user options and imports the nessacary widgets
    def addWidgetsDefault(self, optionFile):
        self.temperatureVar = Label()
        self.add_widget(self.temperatureVar)
        self.temperatureVar.pos = (-275,100)

        self.humidityVar = Label()
        self.add_widget(self.humidityVar)
        self.humidityVar.pos = (275,100)

        self.CO2Var = Label()
        self.add_widget(self.CO2Var)
        self.CO2Var.pos = (-275,-100)

        self.strainVar = Label()
        self.add_widget(self.strainVar)
        self.strainVar.pos = (275,-100)

        self.dayVar = Label()
        self.add_widget(self.dayVar)
        self.dayVar.pos = (0,120)
        self.dayVar.font_size = 55

        self.capture = Button(text="Capture", on_release=lambda a:self.takePicture(self.plantName,self.plantStrain), size_hint=(.25,.1), pos_hint={'x':0.4,'y':0.9})
        self.add_widget(self.capture)

        self.clockDisplay = Label()
        self.add_widget(self.clockDisplay)
        self.clockDisplay.pos = (300,220)
        Clock.schedule_interval(self.update, 1)

#screen where user can pick different options
class optionScreen(Screen):
    def __init__(self, **kwargs):
        super(optionScreen, self).__init__(**kwargs)

        pathway = os.path.dirname(os.path.abspath( __file__ ))
        try:
            optionFile = open(pathway+"/options/GUIOptions.txt","r+")
        except IOError:
            optionFile = createGUIOptions(pathway)

        self.clockDisplay = Label()
        self.add_widget(self.clockDisplay)
        self.clockDisplay.pos = (300,220)
        Clock.schedule_interval(self.update, 1)

    #will update all the variables on screen
    def update(self, dt):
        self.clockDisplay.text = time.asctime()

#main screen
class mainScreen(Screen):
    def __init__(self, **kwargs):
        super(mainScreen, self).__init__(**kwargs)

        self.clockDisplay = Label()
        self.add_widget(self.clockDisplay)
        self.clockDisplay.pos = (300,220)
        Clock.schedule_interval(self.update, 1)

    #will update all the variables on screen
    def update(self, dt):
        self.clockDisplay.text = time.asctime()

#main App GUI control
class ecozoneApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(mainScreen(name="main"))
        sm.add_widget(defaultScreen(name="default"))
        sm.add_widget(optionScreen(name='option'))

        return sm

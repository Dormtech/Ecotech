"""
 * @file mainGUI.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 22 2018
 * @modified June 18 2018
 * @modifiedby SK
 * @brief GUI managment and creation
 */
 """
import kivy
from cameraSequence import camera
from atmSequence import atmosphere
from runMode import deviceControl
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
        #write some more stuff to file

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

    #will update all the variables on screen
    def update(self, dt):
        #call funtion to get info from sensors
        code1Bank = network.readSerial(self.ser,1)

        #Temp sensors
        t1 = deviceControl.sensorValue("T1","C",code1Bank)
        t2 = deviceControl.sensorValue("T2","C",code1Bank)
        t3 = deviceControl.sensorValue("T3","C",code1Bank)
        t4 = deviceControl.sensorValue("T4","C",code1Bank)
        t5 = deviceControl.sensorValue("T5","C",code1Bank)
        #Weighted average
        tempBank = [t1,t2,t3,t4,t5]
        tempWeight = [1,1,1,1,1]
        temp = atmosphere.wAverage(tempBank,tempWeight)
        self.temperatureVar.text = str(temp)
        self.dayVar.text = '00'
        self.clockDisplay.text = time.asctime()


    def takePicture(self):
        try:
            if os.path.isdir("/home/pi/Desktop/Ecotech/RaspberryPi/logs/pics"):
                fileName = "/home/pi/Desktop/Ecotech/RaspberryPi/logs/pics/test" + time.strftime("%d-%y-%m_%H:%M:%S", time.gmtime()) + ".png"
            else:
                os.mkdir("/home/pi/Desktop/Ecotech/RaspberryPi/logs/pics")
                fileName = "/home/pi/Desktop/Ecotech/RaspberryPi/logs/pics/test" + time.strftime("%d-%y-%m_%H:%M:%S", time.gmtime()) + ".png"
            if os.path.isfile(fileName):
                try: #If widget is there
                    os.remove(fileName)
                    time.sleep(0.5)
                    self.remove_widget(self.imgVar)
                    camera.cameraMain(fileName)
                    self.imgVar = Image(source=fileName, pos=(200,75), size_hint=(.5,.5))
                    self.add_widget(self.imgVar)
                except: #if there is no widget
                    os.remove(fileName)
                    time.sleep(0.5)
                    camera.cameraMain(fileName)
                    self.imgVar = Image(source=fileName, pos=(200,75), size_hint=(.5,.5))
                    self.add_widget(self.imgVar)
            else:
                camera.cameraMain(fileName)
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

        self.clockDisplay = Label()
        self.add_widget(self.clockDisplay)
        self.clockDisplay.pos = (300,220)

        self.dayVar = Label()
        self.add_widget(self.dayVar)
        self.dayVar.pos = (0,120)
        self.dayVar.font_size = 55

        self.capture = Button(text="Capture", on_release=lambda a:self.takePicture(), size_hint=(.25,.1), pos_hint={'x':0.4,'y':0.9})
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

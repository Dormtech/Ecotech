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
"""from atmSequence import atmosphere
from control import deviceControl
from networking import network
from logg import deviceLog"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.graph import MeshLinePlot
from kivy.uix.colorpicker import ColorPicker

import random, os, time

from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')


class GUIFunc():

    #creates the option file used to store user config
    def createGUIOptions(pathway):
        optionFile = open(pathway+"/options/GUIOptions.txt","w+")
        
        optionFile.write("c\n")

        return optionFile

#default stats display
class defaultScreen(Screen):
    
    temperatureVar = StringProperty()
    humidityVar = StringProperty()
    CO2Var = StringProperty()
    pHVar = StringProperty()
    dayVar = StringProperty()
    strainVar = StringProperty()


    def __init__(self, **kwargs):
        super(defaultScreen, self).__init__(**kwargs)

        self.makeClock()

        pathway = os.path.dirname(os.path.abspath( __file__ ))
        try:
            optionFile = open(pathway+"/options/GUIOptions.txt","r+")
        except IOError:
            optionFile = createGUIOptions(pathway)

        self.update(1)

        self.addWidgetsDefault(optionFile)
        Clock.schedule_interval(self.update,5)

        #self.ser = network.openSerial()
        self.plantName = "Plant1"
        self.strainVar = "Kush"
        self.dayVar = "01"
        #deviceLog().dayLog(deviceLog().findIndex("dayLog.txt","Machine Start"),"Machine Start","NA",["Machine start up"])

    """
    Makes clock for screen
    """
    def makeClock(self):
        self.clockDisplay = Label(text=time.asctime(), pos=(300,220))
        self.add_widget(self.clockDisplay)
        Clock.schedule_interval(self.updateTime,1)
    def updateTime(self,dt):
        self.clockDisplay.text=time.asctime()
    

    #will update all the variables on screen
    def update(self, dt):
        """sensorBank1 = network.readSerial(self.ser,1)
        temp = self.updateTemp(sensorBank1)
        humid = self.updateHumid(sensorBank1)
        CO2 = self.updateCO2(sensorBank1)
        day = self.updateIndex(self.plantName)"""
        self.temperatureVar = str(random.randint(1,100))
        self.humidityVar =str(random.randint(20,80))
        self.CO2Var =str(random.randint(0,100))
        self.pHVar = str(random.randint(0,14))

        #self.ser = network.openSerial()

    

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

        return str(random.randint(1,100))#atmosphere.wAverage(tempBank,tempWeight)

    #updates the index
    def updateIndex(self):
        index = deviceLog().findIndex("dayLog.txt",self.plantName)
        return index

    #update CO2
    def updateCO2(self,sensorBank):
        c1 = deviceControl().sensorValue("C1","%",sensorBank)
        return c1

    def takePicture(self):
        """try:
            index = deviceLog().findIndex("dayLog.txt",self.plantName)
            stats = ["Tempature=20"]
            deviceLog().dayLog(index,self.plantName,self.strainVar,stats)
            dirHold = os.getcwd().split("/")
            dirHold = dirHold[:-1]
            picDir = "/".join(dirHold) + str("logs/pics")
            if os.path.isdir(picDir) == False:
                os.mkdir(picDir)
            fileName = picDir + "/" + self.plantName + "(" + time.strftime("%d-%y-%m_%H:%M:%S", time.gmtime()) + ").png"
            if os.path.isfile(fileName):
                os.remove(fileName)
                time.sleep(0.1)
                self.remove_widget(self.imgVar)
            deviceControl.captureIMG(fileName)
            self.imgVar = Image(source=fileName, pos=(200,75), size_hint=(.5,.5))
            self.add_widget(self.imgVar)
        except Exception as e:
            errCode = "FAILED TO TAKE PICTURE"
            errMsg = "Failed while attempting to take picture with the following error " + str(e)
            deviceLog().errorLog(errCode,errMsg)"""
        print("flash")

    #reads the user options and imports the nessacary widgets
    def addWidgetsDefault(self, optionFile):
        pass

#screen where user can pick different options
class optionScreen(Screen):
    def __init__(self, **kwargs):
        super(optionScreen, self).__init__(**kwargs)

        pathway = os.path.dirname(os.path.abspath( __file__ ))
        try:
            optionFile = open(pathway+"/options/GUIOptions.txt","r+")
        except IOError:
            optionFile = createGUIOptions(pathway)

        self.makeClock()

        self.colourButton = Button(text="Colour", on_release=lambda a:self.changeColour(),size_hint=(.1,.1), pos=(100,200))


    """
    Makes clock for screen
    """
    def makeClock(self):
        self.clockDisplay = Label(text=time.asctime(), pos=(300,220))
        self.add_widget(self.clockDisplay)
        Clock.schedule_interval(self.updateTime,1)
    def updateTime(self,dt):
        self.clockDisplay.text=time.asctime()


    def changeColour(self):
        pass

    #will update all the variables on screen
    def update(self, dt):
        pass

#main screen
class mainScreen(Screen):

    def __init__(self, **kwargs):
        super(mainScreen, self).__init__(**kwargs)

        self.makeClock()

    """
    Makes clock for screen
    """
    def makeClock(self):
        self.clockDisplay = Label(text=time.asctime(), pos=(300,220))
        self.add_widget(self.clockDisplay)
        Clock.schedule_interval(self.updateTime,1)
    def updateTime(self,dt):
        self.clockDisplay.text=time.asctime()

#main App GUI control
class ecozoneApp(App): 

    def build_config(self, config):
        config.setdefaults('options', {
            'temp': 'C'
        })

    def build(self):
        config = self.config
        sm = ScreenManager()
        sm.add_widget(mainScreen(name="main"))
        sm.add_widget(defaultScreen(name="default"))
        sm.add_widget(optionScreen(name='option'))

        return sm

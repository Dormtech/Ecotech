"""
 * @file mainGUI.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 22 2018
 * @modified Feb 22 2019
 * @modifiedby SK
 * @brief GUI managment and creation
 */
"""
import kivy
"""from atmSequence import atmosphere
from control import deviceControl
from networking import network
from logg import deviceLog"""

from logger import plant_csv
from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, VariableListProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import SettingsWithSidebar
import pandas as pd
from json_settings import settings_json

import random, os, time, threading

from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('kivy', 'keyboard_mode', 'dock')
Config.write()

colour = VariableListProperty()
colour = (1,1,1,0)

strain =StringProperty('None')
name = StringProperty('None')
unitGlob = 'None'

#Camera seperate thread class
class useCamera(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename
    def run(self):
        try:
            """deviceControl.captureIMG(self.fileName)
            self.imgVar = Image(source=self.fileName, pos=(200,75), size_hint=(.5,.5))
            self.add_widget(self.imgVar)"""

            print('flash')
        except Exception as e:
            errCode = "FAILED TO TAKE PICTURE"
            errMsg = "Failed while attempting to take picture with the following error " + str(e)
            deviceLog().errorLog(errCode,errMsg)

#default stats display
class defaultScreen(Screen):

    temperatureVar = StringProperty()
    tempSp = StringProperty()
    humidityVar = StringProperty()
    humiditySp = StringProperty()
    CO2Var = StringProperty()
    pHVar = StringProperty()
    dayVar = StringProperty()
    strainVar = StringProperty()
    plantName = StringProperty()

    def __init__(self, **kwargs):
        super(defaultScreen, self).__init__(**kwargs)

        self.makeClock()

        self.update(1)

        Clock.schedule_interval(self.update,5)

        self.tempSp="25"
        self.humiditySp="60"
        #self.ser = network.openSerial()
        self.plantName = 'test'
        self.dayVar = "01"
        self.strainVar = 'test'
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

    def updateStrain(self):
        global strain
        global name
        self.plantName = str(name)
        self.strainVar = str(strain)

    #will update all the variables on screen
    def update(self, dt):
        """sensorBank1 = network.readSerial(self.ser,1)
        humid = self.updateHumid(sensorBank1)
        CO2 = self.updateCO2(sensorBank1)
        day = self.updateIndex(self.plantName)"""
        global unitGlob

        if unitGlob == 'Imperial':
            self.temperatureVar = str(random.randint(1,100))+chr(176)+'F'
            #self.temperatureVar = self.updateTemp(sensorBank1)+chr(176)+'F'
        else:
            self.temperatureVar = str(random.randint(1,100))+chr(176)+'C'
            #self.temperatureVar = self.updateTemp(sensorBank1)+chr(176)+'C'

        self.humidityVar =str(random.randint(20,80))+"%"
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
            filename = "test.png"
            newThread = useCamera(filename)
            newThread.start()
            newThread.join()

#main screen
class mainScreen(Screen):
    rgba = colour

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

class openingScreen(Screen):
    def __init__(self, **kwargs):
        super(openingScreen, self).__init__(**kwargs)

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

class newPlantScreen(Screen):

    strains = ListProperty()

    if os.name == 'posix':
        fp = open("files/GuiFiles/strains.txt", mode='r')
        strains = fp.readlines()
        strains.sort()
        fp.close()
    else:
        fp = open("files\GuiFiles\strains.txt", mode='r')
        strains = fp.readlines()
        strains.sort()
        fp.close()

    currentStrain = StringProperty('None')
    plantName = StringProperty('')

    def __init__(self, **kwargs):
        super(newPlantScreen, self).__init__(**kwargs)

    #function linked to confirm Button press
    def confirmStrain(self):
        if (self.currentStrain == 'None') | (self.plantName == ''):
            return
        if plant_csv.create_CSV(self.currentStrain, self.plantName) == False:
            #print popupmessage that file exists
            self.manager.current = 'open'
            return

        self.setGlobalGUI()
        self.startBox()
        self.manager.current = 'main'

    #sets Global variables for the Gui to use
    def setGlobalGUI(self):
        global strain
        global name
        global fp

        strain = self.currentStrain
        name = self.plantName

    #starts the nessacry programs to operate all box functions
    def startBox(self):
        Clock.schedule_interval(ecozoneApp.boxFunctions,5)
        pass

class continuePlantScreen(Screen):

    plants = ListProperty()

    if os.name == 'posix':
        fp = open("files/GuiFiles/plants.txt", mode='r')
    else:
        fp = open("files\GuiFiles\plants.txt", mode='r')
    plants = fp.readlines()
    fp.close()

    currentPlant = StringProperty('')

    def __init__(self, **kwargs):
        super(continuePlantScreen, self).__init__(**kwargs)

    def confirmPlant(self):
        if self.currentPlant == '':
            return
        self.manager.current = 'main'

    #sets Global variables for the Gui to use
    def setGlobalGUI(self):
        global name
        global strain
        global fp

        name = self.currentPlant

        strain = plant_csv.getStrain()

    #starts the nessacry programs to operate all box functions
    def startBox(self):
        Clock.schedule_interval(ecozoneApp.boxFunctions,5)
        pass

#main App GUI control
class ecozoneApp(App):

    def build_config(self, config):
        config.setdefaults("Basic", {
            "Units":"Metric", 'colour':'Black'
            })

    def build_settings(self, settings):
        settings.add_json_panel('Options', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        global unitGlob

        if key == 'Units':
            if value == 'Imperial':
                unitGlob = 'Imperial'
            else:
                unitGlob = 'Metric'

    def boxFunctions(self):
        print('box stuff')

    def build(self):
        global unitGlob
        self.use_kivy_settings = False
        self.settings_cls = SettingsWithSidebar
        unitGlob = self.config.get('Basic', 'Units')
        sm = ScreenManager()
        sm.add_widget(openingScreen(name="open"))
        sm.add_widget(newPlantScreen(name='newPlantS'))
        sm.add_widget(continuePlantScreen(name='continuePlantS'))
        sm.add_widget(mainScreen(name="main"))
        sm.add_widget(defaultScreen(name="default"))
        return sm

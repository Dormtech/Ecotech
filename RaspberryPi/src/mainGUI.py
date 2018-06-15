"""
 * @file mainGUI.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 22 2018
 * @modified June 15 2018
 * @modifiedby SK
 * @brief GUI managment and creation
 */
 """
import kivy


from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
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


class GUIFunc():
    
    #creates the option file used to store user config
    def createGUIOptions(pathway):
        optionFile = open(pathway+"/options/GUIOptions.txt","w+")
        #write some more stuff to file

        return optionFile


#default "screen saver"
class defaultScreen(Screen):

    def __init__(self, **kwargs):
        super(defaultScreen, self).__init__(**kwargs)   

        pathway = os.path.dirname(os.path.abspath( __file__ ))
        try:
            optionFile = open(pathway+"/options/GUIOptions.txt","r+")
        except IOError:
            optionFile = createGUIOptions(pathway)  

        self.plot = MeshLinePlot(color=[1, 0, 0, 1])  
        self.ids.graph.add_plot(self.plot)
        self.addWidgetsDefault(optionFile)
        Clock.schedule_interval(self.update, 1)

    #will update all the variables on screen
    def update(self, dt):
        #call funtion to get info from sensors
        self.temperatureVar.text = str(random.randint(0,200))
        self.dayVar.text = '00'
        self.clockDisplay.text = time.asctime()
        self.plot.points = [(4, 2)]

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
                
        return sm

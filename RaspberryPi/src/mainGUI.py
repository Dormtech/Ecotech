"""
 * @file mainGUI.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 22 2018
 * @modified May 31 2018
 * @modifiedby SK
 * @brief GUI managment and creation
 */
 """
import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ObjectProperty 
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen


import random, os

class GUIFunc():
    #creates the option file used to store user config
    def createGUIOptions(pathway):
        optionFile = open(pathway+"/options/GUIOptions.txt","w+")
        #write some more stuff to file

        return optionFile


#default "screen saver"
class defaultScreenLayout(GridLayout):

    def __init__(self, **kwargs):
        super(defaultScreenLayout, self).__init__(**kwargs)   

        pathway = os.path.dirname(os.path.abspath( __file__ ))
        try:
            optionFile = open(pathway+"/options/GUIOptions.txt","r+")
        except IOError:
            optionFile = createGUIOptions(pathway)    

        self.temperatureVar = Label()
        self.add_widget(self.temperatureVar)
        Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        #call funtion to get info from sensors

        self.temperatureVar.text = str(random.randint(0,200))


#main App GUI control
class ecozoneApp(App):

    def build(self):
        return defaultScreenLayout()

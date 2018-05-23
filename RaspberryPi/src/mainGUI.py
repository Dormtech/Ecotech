"""
 * @file mainGUI.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 22 2018
 * @modified May 22 2018
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
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock


import random

##https://github.com/kivy/kivy/wiki/Data-driven-variables-with-kivy-properties##

#default "screen saver"
class defaultDisplay(Widget):
    

    def __init__(self, **kwargs):
        super(defaultDisplay, self).__init__(**kwargs)
        event = Clock.schedule_interval(self.getTemp,1/1.)
        temperatureVar = StringProperty('')
        self.getTemp()
        self.add_widget()
    
    def getTemp(self):
        temperatureVar = str(random.randint(1,10))

#main App GUI control
class ecozone(App):

    def build(self):
        return defaultDisplay()

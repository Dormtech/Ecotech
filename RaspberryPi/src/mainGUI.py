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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

class ecozone(App):

    def build(self):
        return Label(text='Hello world')

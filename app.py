#!/bin/env python3
from cocos.director import director
from menus import MainMenu
from singletons import *


class App:
    def __init__(self):
        self.vendor = Vendor()
        self.main_menu = MainMenu()

    def start(self):
        director.init(resizable=False)
        director.run(self.main_menu)


if __name__ == '__main__':
    App().start()

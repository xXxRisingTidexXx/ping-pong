from globals import RM
from factory import prepare_tk
from menus import MainMenu
from time import sleep


class App:
    def __init__(self):
        data = RM[RM.APP]
        self.tk = prepare_tk(data['tk'])
        self.delay = data['delay']
        self.main_menu = MainMenu(self.tk)

    def start(self):
        while self.main_menu.active:
            self.tk.update_idletasks()
            self.tk.update()
            sleep(self.delay)


if __name__ == '__main__':
    App().start()

from globals import CACHE, Screen
from factory import *
from game import Game, Session


class Menu(Screen):
    def __init__(self, tk, name):
        super().__init__(tk, name)
        self.frame = place_frame(self.tk, self.data['frame'])


class VisualizableMenu(Menu):
    def __init__(self, tk, name):
        super().__init__(tk, name)
        self.hidden = False
        self.info = None

    def hide(self):
        if not self.hidden:
            self.hidden = True
            self.info = self.frame.place_info()
            self.frame.place_forget()

    def visualize(self):
        if self.hidden:
            self.hidden = False
            self.frame.place(self.info)


class MainMenu(VisualizableMenu):
    def __init__(self, tk):
        super().__init__(tk, RM.MAIN_MENU)
        self.active = True
        self.buttons = self.prepare_buttons(self.data['buttons'])
        self.info_menu = None
        self.help_menu = None

    def prepare_buttons(self, data):
        return (
            pack_button(self.frame, data['play_button'], self.__play),
            pack_button(self.frame, data['info_button'], self.__info),
            pack_button(self.frame, data['help_button'], self.__help),
            pack_button(self.frame, data['exit_button'], self.__exit)
        )

    def __play(self):
        self.hide()
        SummaryMenu(self, Game(self).play())

    def __info(self):
        self.hide()
        if self.info_menu is None:
            self.info_menu = InfoMenu(self)
        else:
            self.info_menu.update()
        self.info_menu.visualize()

    def __help(self):
        self.hide()
        if self.help_menu is None:
            self.help_menu = HelpMenu(self)
        self.help_menu.visualize()

    def __exit(self):
        CACHE.save(RM.RESULTS, RM.PATHS[RM.RESULTS])
        self.active = False


class SummaryMenu(Menu):
    def __init__(self, main_menu, session):
        super().__init__(main_menu.tk, RM.SUMMARY_MENU)
        self.main_menu = main_menu
        self.session = session
        self.statistics = Statistics(self.frame, self.data['statistics'], self.session)
        self.ok_button = grid_button(self.frame, self.data['ok_button'], self.__ok)

    def __ok(self):
        if self.statistics.filled():
            CACHE.update(RM.RESULTS, self.statistics.get_result(), self.__appender)
            self.frame.place_forget()
            self.main_menu.visualize()

    # noinspection PyMethodMayBeStatic
    def __appender(self, lst, value):
        lst.append(value)
        return lst


class Statistics:
    def __init__(self, master, data, session):
        self.master = master
        self.header = grid_label(self.master, data['header_label'])
        self.duration = self.prepare_pair(data['duration'], session[Session.DURATION])
        self.score = self.prepare_pair(data['score'], session[Session.SCORE])
        self.name = self.prepare_input(data['name'])

    def prepare_pair(self, data, value_text):
        key_label = grid_label(self.master, data['key_label'])
        value_label = grid_label(self.master, data['value_label'])
        value_label.configure(text=value_text)
        return key_label, value_label

    def prepare_input(self, data):
        key_label = grid_label(self.master, data['key_label'])
        entry = grid_entry(self.master, data['entry'])
        entry.focus()
        return key_label, entry

    def filled(self):
        return len(self.name[1].get()) > 0

    def get_result(self):
        return {'name': self.name[1].get(), 'result': self.score[1]['text']}


class InfoMenu(VisualizableMenu):
    def __init__(self, main_menu):
        super().__init__(main_menu.tk, RM.INFO_MENU)
        self.main_menu = main_menu
        self.table = Table(self.frame, self.data['table'])
        self.back_button = pack_button(self.frame, self.data['back_button'], self.__back)

    def __back(self):
        self.hide()
        self.main_menu.visualize()

    def update(self):
        self.table.update()


class Table:
    def __init__(self, master, data):
        self.master = master
        self.rows = data['rows']
        self.header_label = pack_label(self.master, data['header_label'])
        self.carcass = self.prepare_carcass(data['separator'], data['name_label'], data['result_label'])
        self.update()

    # noinspection PyUnusedLocal
    def prepare_carcass(self, separator_data, name_label_data, result_label_data):
        return [{
            'separator': pack_separator(self.master, separator_data),
            'name_label': pack_label(self.master, name_label_data),
            'result_label': pack_label(self.master, result_label_data)
        } for i in range(self.rows)]

    def update(self):
        content = self.limit(CACHE[RM.RESULTS])
        CACHE[RM.RESULTS] = content
        self.fill(content)

    def limit(self, content):
        return sorted(content, key=lambda r: r['result'], reverse=True)[:self.rows]

    def fill(self, content):
        for i in range(self.rows):
            self.carcass[i]['name_label'].configure(text=content[i]['name'])
            self.carcass[i]['result_label'].configure(text=content[i]['result'])


class HelpMenu(VisualizableMenu):
    def __init__(self, main_menu):
        super().__init__(main_menu.tk, RM.HELP_MENU)
        self.main_menu = main_menu
        self.header_label = pack_label(self.frame, self.data['header_label'])
        self.wrapper_label = pack_label(self.frame, self.data['wrapper_label'])
        self.back_button = pack_button(self.frame, self.data['back_button'], self.__back)

    def __back(self):
        self.hide()
        self.main_menu.visualize()

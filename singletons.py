from yaml import load, dump
from pathlib import Path
#
#
# # noinspection PyMethodMayBeStatic
# class Rm:
#     FONTS = 'fonts'
#     STYLES = 'styles'
#     POSITIONS = 'positions'
#     RESULTS = 'results'
#     APP = 'app'
#     MAIN_MENU = 'main_menu'
#     SUMMARY_MENU = 'summary_menu'
#     INFO_MENU = 'info_menu'
#     HELP_MENU = 'help_menu'
#     GAME = 'game'
#     PATHS = {
#         FONTS: 'res/fonts.yaml',
#         STYLES: 'res/styles.yaml',
#         POSITIONS: 'res/positions.yaml',
#         RESULTS: 'res/results.yaml',
#         APP: 'res/app.yaml',
#         MAIN_MENU: 'res/main_menu.yaml',
#         SUMMARY_MENU: 'res/summary_menu.yaml',
#         INFO_MENU: 'res/info_menu.yaml',
#         HELP_MENU: 'res/help_menu.yaml',
#         GAME: 'res/game.yaml'
#     }
#
#     def __init__(self):
#         self.data = {k: self.read(obj) for k, obj in Rm.PATHS.items()}
#
#     def __getitem__(self, res):
#         return self.data[res]
#
#     def read(self, path):
#         with open(path) as stream:
#             return load(stream)
#
#     def write(self, data, path):
#         with open(path, 'w') as stream:
#             dump(data, stream, default_flow_style=False)
#
#
# RM = Rm()
#
#
# class Cache:
#     def __init__(self, rm):
#         self.rm = rm
#         self.data = {Rm.RESULTS: self.rm[Rm.RESULTS]}
#
#     def __getitem__(self, key):
#         return self.data[key]
#
#     def __setitem__(self, key, value):
#         self.data[key] = value
#
#     def update(self, key, value, updater):
#         self[key] = updater(self[key], value)
#
#     def save(self, key, path):
#         self.rm.write(self[key], path)
#
#
# CACHE = Cache(RM)
#
#
# class Screen:
#     def __init__(self, tk, name):
#         self.tk = tk
#         self.data = RM[name]
# from tkinter import *
# from tkinter.ttk import Separator
# from globals import RM
#
#
# def prepare_tk(data):
#     tk = Tk()
#     tk.title(data['title'])
#     tk.geometry('{}x{}'.format(tk.winfo_screenwidth(), tk.winfo_screenheight()))
#     tk.resizable(data['resizable']['width'], data['resizable']['height'])
#     tk.wm_attributes(*data['wm_attributes'])
#     tk.configure(background=data['background'])
#     return tk
#
#
# def prepare_button(master, data, command):
#     button = Button(master, RM[RM.STYLES][data['style']])
#     button.configure(text=data['text'], font=RM[RM.FONTS][data['font']], command=command)
#     return button
#
#
# def prepare_label(master, data):
#     label = Label(master, RM[RM.STYLES][data['style']])
#     label.configure(text=data['text'], font=RM[RM.FONTS][data['font']])
#     return label
#
#
# def place_frame(master, data):
#     frame = Frame(master, RM[RM.STYLES][data['style']])
#     frame.place(RM[RM.POSITIONS][data['position']])
#     frame.update()
#     return frame
#
#
# def pack_button(master, data, command):
#     button = prepare_button(master, data, command)
#     button.pack(RM[RM.POSITIONS][data['position']])
#     button.update()
#     return button
#
#
# def pack_label(master, data):
#     label = prepare_label(master, data)
#     label.pack(RM[RM.POSITIONS][data['position']])
#     label.update()
#     return label
#
#
# def pack_separator(master, data):
#     separator = Separator(master, orient=data['orient'])
#     separator.pack(RM[RM.POSITIONS][data['position']])
#     return separator
#
#
# def pack_canvas(master, data):
#     canvas = Canvas(master, width=master.winfo_width(), height=master.winfo_height())
#     canvas.configure(RM[RM.STYLES][data['style']])
#     canvas.pack(RM[RM.POSITIONS][data['position']])
#     canvas.update()
#     return canvas
#
#
# def grid_button(master, data, command):
#     button = prepare_button(master, data, command)
#     button.grid(RM[RM.POSITIONS][data['position']])
#     button.update()
#     return button
#
#
# def grid_label(master, data):
#     label = prepare_label(master, data)
#     label.grid(RM[RM.POSITIONS][data['position']])
#     label.update()
#     return label
#
#
# def grid_entry(master, data):
#     entry = Entry(master, RM[RM.STYLES][data['style']])
#     entry.configure(font=RM[RM.FONTS][data['font']])
#     entry.grid(RM[RM.POSITIONS][data['position']])
#     entry.update()
#     return entry
#
#
# def create_line(canvas, data):
#     _id = canvas.create_line(data['x1'], data['y1'], data['x2'], data['y2'], RM[RM.STYLES][data['style']])
#     canvas.move(_id, data['x0'], data['y0'])
#     return _id
#
#
# def create_rectangle(canvas, data):
#     _id = canvas.create_rectangle(data['x1'], data['y1'], data['x2'], data['y2'], RM[RM.STYLES][data['style']])
#     canvas.move(_id, data['x0'], data['y0'])
#     return _id
#
#
# def create_oval(canvas, data):
#     _id = canvas.create_oval(data['x1'], data['y1'], data['x2'], data['y2'], RM[RM.STYLES][data['style']])
#     canvas.move(_id, data['x0'], data['y0'])
#     return _id
#
#
# def create_text(canvas, data):
#     _id = canvas.create_text(data['x1'], data['y1'], text=data['value'], font=RM[RM.FONTS][data['font']])
#     canvas.itemconfigure(_id, RM[RM.STYLES][data['style']])
#     return _id


class Vendor:
    obj = None
    FONTS = 'fonts'
    STYLES = 'styles'
    POSITIONS = 'positions'
    RESULTS = 'results'
    APP = 'app'
    MAIN_MENU = 'main_menu'
    SUMMARY_MENU = 'summary_menu'
    INFO_MENU = 'info_menu'
    HELP_MENU = 'help_menu'
    GAME = 'game'

    def __init__(self):
        self.paths = {
            Vendor.FONTS: Path('res/fonts.yaml'),
            Vendor.STYLES: 'res/styles.yaml',
            Vendor.POSITIONS: 'res/positions.yaml',
            Vendor.RESULTS: 'res/results.yaml',
            Vendor.APP: 'res/app.yaml',
            Vendor.MAIN_MENU: 'res/main_menu.yaml',
            Vendor.SUMMARY_MENU: 'res/summary_menu.yaml',
            Vendor.INFO_MENU: 'res/info_menu.yaml',
            Vendor.HELP_MENU: 'res/help_menu.yaml',
            Vendor.GAME: 'res/game.yaml'
        }

    def _results_exists(self):
        return

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
        return cls.obj

    def __getitem__(self, key):
        pass

    def load(self, path):
        pass

    def dump(self, data, path):
        pass


class Cache:
    def __init__(self, vendor):
        self.vendor = vendor
        pass

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value, setter=None):
        pass

    def save(self, key, path):
        pass


class Forge:
    def __init__(self, vendor):
        self.vendor = vendor
        pass

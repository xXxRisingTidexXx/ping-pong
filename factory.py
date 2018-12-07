from tkinter import *
from tkinter.ttk import Separator
from globals import RM


def prepare_tk(data):
    tk = Tk()
    tk.title(data['title'])
    tk.geometry('{}x{}'.format(tk.winfo_screenwidth(), tk.winfo_screenheight()))
    tk.resizable(data['resizable']['width'], data['resizable']['height'])
    tk.wm_attributes(*data['wm_attributes'])
    tk.configure(background=data['background'])
    return tk


def prepare_button(master, data, command):
    button = Button(master, RM[RM.STYLES][data['style']])
    button.configure(text=data['text'], font=RM[RM.FONTS][data['font']], command=command)
    return button


def prepare_label(master, data):
    label = Label(master, RM[RM.STYLES][data['style']])
    label.configure(text=data['text'], font=RM[RM.FONTS][data['font']])
    return label


def place_frame(master, data):
    frame = Frame(master, RM[RM.STYLES][data['style']])
    frame.place(RM[RM.POSITIONS][data['position']])
    frame.update()
    return frame


def pack_button(master, data, command):
    button = prepare_button(master, data, command)
    button.pack(RM[RM.POSITIONS][data['position']])
    button.update()
    return button


def pack_label(master, data):
    label = prepare_label(master, data)
    label.pack(RM[RM.POSITIONS][data['position']])
    label.update()
    return label


def pack_separator(master, data):
    separator = Separator(master, orient=data['orient'])
    separator.pack(RM[RM.POSITIONS][data['position']])
    return separator


def pack_canvas(master, data):
    canvas = Canvas(master, width=master.winfo_width(), height=master.winfo_height())
    canvas.configure(RM[RM.STYLES][data['style']])
    canvas.pack(RM[RM.POSITIONS][data['position']])
    canvas.update()
    return canvas


def grid_button(master, data, command):
    button = prepare_button(master, data, command)
    button.grid(RM[RM.POSITIONS][data['position']])
    button.update()
    return button


def grid_label(master, data):
    label = prepare_label(master, data)
    label.grid(RM[RM.POSITIONS][data['position']])
    label.update()
    return label


def grid_entry(master, data):
    entry = Entry(master, RM[RM.STYLES][data['style']])
    entry.configure(font=RM[RM.FONTS][data['font']])
    entry.grid(RM[RM.POSITIONS][data['position']])
    entry.update()
    return entry


def create_line(canvas, data):
    return create(canvas, data, canvas.create_line)


def create(canvas, data, creator):
    _id = creator(data['x1'], data['y1'], data['x2'], data['y2'], RM[RM.STYLES][data['style']])
    canvas.move(_id, data['x0'], data['y0'])
    return _id


def create_rectangle(canvas, data):
    return create(canvas, data, canvas.create_rectangle)


def create_oval(canvas, data):
    return create(canvas, data, canvas.create_oval)


def create_text(canvas, data):
    return create(canvas, data, canvas.create_text)

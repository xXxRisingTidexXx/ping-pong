from random import choice
from time import sleep
from tkinter import *
from tkinter.ttk import Separator
from yaml import load, dump


# Maybe it'll be better to create all-game cache for different temporary data
class App:
    DATA_PATH = 'res/app.yaml'

    def __init__(self):
        self.rm = RM()
        self.wm = WM(self.rm)
        self.cache = Cache(self.rm)
        data = self.rm[App]
        self.tk = self.wm.prepare_tk(data['tk'])
        self.delay = data['delay']
        self.main_menu = MainMenu(self.rm, self.wm, self.cache, self.tk)

    def start(self):
        while self.main_menu.active:
            self.tk.update_idletasks()
            self.tk.update()
            sleep(self.delay)


class RM:
    FONTS = 'fonts'
    STYLES = 'styles'
    POSITIONS = 'positions'

    def __init__(self):
        self.data = {
            RM.FONTS: self.read('res/fonts.yaml'),
            RM.STYLES: self.read('res/styles.yaml'),
            RM.POSITIONS: self.read('res/positions.yaml'),
            App: self.read(App.DATA_PATH),
            MainMenu: self.read(MainMenu.DATA_PATH),
            Game: self.read(Game.DATA_PATH),
            # Summary: self.read(Summary.DATA_PATH),
            InfoMenu: self.read(InfoMenu.DATA_PATH),
            HelpMenu: self.read(HelpMenu.DATA_PATH)
        }

    def __getitem__(self, res):
        return self.data[res]

    # noinspection PyMethodMayBeStatic
    def read(self, path):
        with open(path) as stream:
            return load(stream)

    # noinspection PyMethodMayBeStatic
    def write(self, data, path):
        with open(path, 'w') as stream:
            dump(data, stream, default_flow_style=False)


class WM:
    def __init__(self, rm):
        self.rm = rm

    # noinspection PyMethodMayBeStatic
    def prepare_tk(self, data):
        tk = Tk()
        tk.title(data['title'])
        tk.geometry('{}x{}'.format(tk.winfo_screenwidth(), tk.winfo_screenheight()))
        tk.resizable(data['resizable']['width'], data['resizable']['height'])
        tk.wm_attributes(*data['wm_attributes'])
        tk.configure(background=data['background'])
        return tk

    def prepare_frame(self, master, data):
        frame = Frame(master, self.rm[RM.STYLES][data['style']])
        frame.place(self.rm[RM.POSITIONS][data['position']])
        frame.update()
        return frame

    def prepare_button(self, master, data, command):
        button = Button(master, self.rm[RM.STYLES][data['style']])
        button.configure(text=data['text'], font=self.rm[RM.FONTS][data['font']], command=command)
        button.pack(self.rm[RM.POSITIONS][data['position']])
        button.update()
        return button

    # noinspection PyMethodMayBeStatic
    def prepare_canvas(self, master, data, width, height):
        canvas = Canvas(master, width=width, height=height)
        canvas.configure(data)
        canvas.pack()
        canvas.update()
        return canvas

    def prepare_label(self, master, data):
        label = Label(master, self.rm[RM.STYLES][data['style']])
        label.configure(text=data['text'], font=self.rm[RM.FONTS][data['font']])
        label.pack(self.rm[RM.POSITIONS][data['position']])
        label.update()
        return label

    def prepare_separator(self, master, data):
        separator = Separator(master, orient=data['orient'])
        separator.pack(self.rm[RM.POSITIONS][data['position']])
        return separator


class Cache:
    def __init__(self, rm):
        self.rm = rm
        self.data = {Table.CONTENT: self.rm.read(Table.CONTENT_PATH)}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def update(self, key, value, updater):
        self[key] = updater(self[key], value)

    def save(self, key, path):
        self.rm.write(self[key], path)


class Menu:
    def __init__(self, rm, wm, tk):
        self.rm = rm
        self.wm = wm
        self.tk = tk
        self.hidden = False
        self.frame = None
        self.frame_place_info = None

    def hide(self):
        if not self.hidden:
            self.hidden = True
            self.frame_place_info = self.frame.place_info()
            self.frame.place_forget()

    def visualize(self):
        if self.hidden:
            self.hidden = False
            self.frame.place(self.frame_place_info)


class MainMenu(Menu):
    DATA_PATH = 'res/main_menu.yaml'

    def __init__(self, rm, wm, cache, tk):
        super().__init__(rm, wm, tk)
        self.cache = cache
        self.active = True
        data = self.rm[MainMenu]
        self.frame = self.wm.prepare_frame(self.tk, data['frame'])
        self.buttons = self.prepare_buttons(data['buttons'])
        self.last_player = {'name': 'Danya', 'result': 5}  # later we will delete it
        self.info_menu = None
        self.help_menu = None

    def prepare_buttons(self, data):
        return (
            self.wm.prepare_button(self.frame, data['play_button'], self.__play),
            self.wm.prepare_button(self.frame, data['info_button'], self.__info),
            self.wm.prepare_button(self.frame, data['help_button'], self.__help),
            self.wm.prepare_button(self.frame, data['exit_button'], self.__exit)
        )

    def __play(self):
        self.hide()
        Game(self).play()  # later we will extract game statistics from cache, and self.last_player will be deleted
        self.cache.update(Table.CONTENT, self.last_player, self.__appender)

    # noinspection PyMethodMayBeStatic
    def __appender(self, lst, value):
        lst.append(value)
        return lst

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
        self.cache.save(Table.CONTENT, Table.CONTENT_PATH)
        self.active = False


class Game:
    DATA_PATH = 'res/game.yaml'

    def __init__(self, main_menu):
        self.rm = main_menu.rm
        self.wm = main_menu.wm
        self.tk = main_menu.tk
        self.main_menu = main_menu
        data = self.rm[Game]
        self.delay = data['delay']
        self.canvas = self.wm.prepare_canvas(self.tk, data['canvas'], self.tk.winfo_width(), self.tk.winfo_height())
        # self.score_label = self.wm.prepare_label(self.canvas, data['score_label'])
        self.paddle = Paddle(self.canvas, data['paddle'])
        self.ball = Ball(self.canvas, data['ball'], self.paddle.id, self.delay)

    def play(self):
        while self.ball.flies():
            self.ball.move()
            self.tk.update_idletasks()
            self.tk.update()
            sleep(self.delay)
        self.canvas.pack_forget()
        self.main_menu.visualize()  # delete it later
        # Summary(self.rm, self.tk, self.main_menu, ...)  put statistics here


class Paddle:
    def __init__(self, canvas, data):
        self.canvas = canvas
        self.id = self.prepare_rectangle(data['rectangle'])
        self.dxl = data['dxl']
        self.dxr = data['dxr']
        self.canvas.bind_all(data['left_arrow'], self.__move_left)
        self.canvas.bind_all(data['right_arrow'], self.__move_right)

    def prepare_rectangle(self, data):
        _id = self.canvas.create_rectangle(data['x1'], data['y1'], data['x2'], data['y2'], data['style'])
        self.canvas.move(_id, data['x0'], data['y0'])
        return _id

    # noinspection PyUnusedLocal
    def __move_left(self, event):
        self.canvas.move(self.id, self.dxl if self.hit_left_border() else 0, 0)

    def hit_left_border(self):
        return self.canvas.coords(self.id)[0] > 0

    # noinspection PyUnusedLocal
    def __move_right(self, event):
        self.canvas.move(self.id, self.dxr if self.hit_right_border() else 0, 0)

    def hit_right_border(self):
        return self.canvas.coords(self.id)[2] < self.canvas.winfo_width()


class Ball:
    def __init__(self, canvas, data, paddle_id, dt):
        self.canvas = canvas
        self.id = self.prepare_oval(data['oval'])
        self.paddle_id = paddle_id
        self.dx = choice(data['dx'])
        self.dy = choice(data['dy'])
        self.dt = dt

    def prepare_oval(self, data):
        _id = self.canvas.create_oval(data['x1'], data['y1'], data['x2'], data['y2'], data['style'])
        self.canvas.move(_id, data['x0'], data['y0'])
        return _id

    def flies(self):
        return self.canvas.coords(self.id)[1] <= self.canvas.winfo_height()

    def move(self):
        coords = self.canvas.coords(self.id)
        self.dx = self.move_x(coords)
        self.dy = self.move_y(coords)
        self.canvas.move(self.id, self.dx, self.dy)

    def move_x(self, coords):
        return 1 if self.hit_left_border(coords) else -1 if self.hit_right_border(coords) else self.dx

    # noinspection PyMethodMayBeStatic
    def hit_left_border(self, coords):
        return coords[0] <= 0

    def hit_right_border(self, coords):
        return coords[2] >= self.canvas.winfo_width()

    def move_y(self, coords):
        return 1 if self.hit_top_border(coords) else -1 if self.hit_paddle(coords) else self.dy

    # noinspection PyMethodMayBeStatic
    def hit_top_border(self, coords):
        return coords[1] <= 0

    def hit_paddle(self, coords):
        paddle_coords = self.canvas.coords(self.paddle_id)
        return self.upon_paddle(coords, paddle_coords) and self.touch_paddle(coords, paddle_coords)

    # noinspection PyMethodMayBeStatic
    def upon_paddle(self, coords, paddle_coords):
        return coords[2] >= paddle_coords[0] and coords[0] <= paddle_coords[2]

    # noinspection PyMethodMayBeStatic
    def touch_paddle(self, coords, paddle_coords):
        return paddle_coords[1] <= coords[3] <= paddle_coords[3]

# class Summary:
#     DATA_PATH = 'res/summary.yaml'
#
#     def __init__(self, rm, tk, main_menu, statistics):
#         self.rm = rm
#         self.tk = tk
#         self.main_menu = main_menu
#         data = self.rm[Summary]
#         self.frame = self.main_menu.prepare_frame(...)
#         pass
#
#     def __ok(self):
#         self.frame.place_forget()
#         self.main_menu.last_player = (...)
#         self.main_menu.visualize()
#         pass


class InfoMenu(Menu):
    DATA_PATH = 'res/info_menu.yaml'

    def __init__(self, main_menu):
        super().__init__(main_menu.rm, main_menu.wm, main_menu.tk)
        data = self.rm[InfoMenu]
        self.frame = self.wm.prepare_frame(self.tk, data['frame'])
        self.table = Table(self, main_menu.cache, data['table'])
        self.back_button = self.wm.prepare_button(self.frame, data['back_button'], self.__back)
        self.main_menu = main_menu

    def __back(self):
        self.hide()
        self.main_menu.visualize()

    def update(self):
        self.table.update()


class Table:
    CONTENT = 'content'
    CONTENT_PATH = 'res/table.yaml'

    def __init__(self, info_menu, cache, data):
        self.info_menu = info_menu
        self.cache = cache
        self.rows = data['rows']
        self.header_label = self.info_menu.wm.prepare_label(self.info_menu.frame, data['header_label'])
        self.carcass = self.prepare_carcass(data['separator'], data['name_label'], data['result_label'])
        self.update()

    # noinspection PyUnusedLocal
    def prepare_carcass(self, separator_data, name_label_data, result_label_data):
        return [{
            'separator': self.info_menu.wm.prepare_separator(self.info_menu.frame, separator_data),
            'name_label': self.info_menu.wm.prepare_label(self.info_menu.frame, name_label_data),
            'result_label': self.info_menu.wm.prepare_label(self.info_menu.frame, result_label_data)
        } for i in range(self.rows)]

    def update(self):
        content = self.limit(self.cache[Table.CONTENT])
        self.fill(content)
        self.cache[Table.CONTENT] = content

    def fill(self, content):
        for i in range(self.rows):
            self.carcass[i]['name_label'].configure(text=content[i]['name'])
            self.carcass[i]['result_label'].configure(text=content[i]['result'])

    def limit(self, content):
        return sorted(content, key=lambda r: r['result'], reverse=True)[:self.rows]


class HelpMenu(Menu):
    DATA_PATH = 'res/help_menu.yaml'

    def __init__(self, main_menu):
        super().__init__(main_menu.rm, main_menu.wm, main_menu.tk)
        data = self.rm[HelpMenu]
        self.frame = self.wm.prepare_frame(self.tk, data['frame'])
        self.header_label = self.wm.prepare_label(self.frame, data['header_label'])
        self.wrapper_label = self.wm.prepare_label(self.frame, data['wrapper_label'])
        self.back_button = self.wm.prepare_button(self.frame, data['back_button'], self.__back)
        self.main_menu = main_menu

    def __back(self):
        self.hide()
        self.main_menu.visualize()


if __name__ == '__main__':
    App().start()

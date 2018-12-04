from random import choice
from time import sleep, time, strftime, gmtime
from tkinter import *
from tkinter.ttk import Separator
from yaml import load, dump


class App:
    DATA_PATH = 'res/app.yaml'
    RESOURCE_MANAGER = None
    WIDGET_MANAGER = None
    CACHE = None

    def __init__(self):
        App.RESOURCE_MANAGER = ResourceManager()
        App.WIDGET_MANAGER = WidgetManager()
        App.CACHE = Cache()
        data = App.RESOURCE_MANAGER[App]
        self.tk = App.WIDGET_MANAGER.prepare_tk(data['tk'])
        self.delay = data['delay']
        self.main_menu = MainMenu(self.tk)

    def start(self):
        while self.main_menu.active:
            self.tk.update_idletasks()
            self.tk.update()
            sleep(self.delay)


class ResourceManager:
    FONTS = 'fonts'
    STYLES = 'styles'
    POSITIONS = 'positions'

    def __init__(self):
        self.data = {
            ResourceManager.FONTS: self.read('res/fonts.yaml'),
            ResourceManager.STYLES: self.read('res/styles.yaml'),
            ResourceManager.POSITIONS: self.read('res/positions.yaml'),
            App: self.read(App.DATA_PATH),
            MainMenu: self.read(MainMenu.DATA_PATH),
            Game: self.read(Game.DATA_PATH),
            SummaryMenu: self.read(SummaryMenu.DATA_PATH),
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


# noinspection PyMethodMayBeStatic
class WidgetManager:
    def prepare_tk(self, data):
        tk = Tk()
        tk.title(data['title'])
        tk.geometry('{}x{}'.format(tk.winfo_screenwidth(), tk.winfo_screenheight()))
        tk.resizable(data['resizable']['width'], data['resizable']['height'])
        tk.wm_attributes(*data['wm_attributes'])
        tk.configure(background=data['background'])
        return tk

    def place_frame(self, master, data):
        frame = Frame(master, App.RESOURCE_MANAGER[ResourceManager.STYLES][data['style']])
        frame.place(App.RESOURCE_MANAGER[ResourceManager.POSITIONS][data['position']])
        frame.update()
        return frame

    def pack_button(self, master, data, command):
        button = Button(master, App.RESOURCE_MANAGER[ResourceManager.STYLES][data['style']])
        button.configure(
            text=data['text'], font=App.RESOURCE_MANAGER[ResourceManager.FONTS][data['font']], command=command
        )
        button.pack(App.RESOURCE_MANAGER[ResourceManager.POSITIONS][data['position']])
        button.update()
        return button

    def pack_canvas(self, master, data):
        canvas = Canvas(master, width=master.winfo_width(), height=master.winfo_height())
        canvas.configure(App.RESOURCE_MANAGER[ResourceManager.STYLES][data['style']])
        canvas.pack(App.RESOURCE_MANAGER[ResourceManager.POSITIONS][data['position']])
        canvas.update()
        return canvas

    def grid_label(self, master, data):
        pass

    def pack_label(self, master, data):
        label = Label(master, App.RESOURCE_MANAGER[ResourceManager.STYLES][data['style']])
        label.configure(text=data['text'], font=App.RESOURCE_MANAGER[ResourceManager.FONTS][data['font']])
        label.pack(App.RESOURCE_MANAGER[ResourceManager.POSITIONS][data['position']])
        label.update()
        return label

    def pack_separator(self, master, data):
        separator = Separator(master, orient=data['orient'])
        separator.pack(App.RESOURCE_MANAGER[ResourceManager.POSITIONS][data['position']])
        return separator


class Cache:
    def __init__(self):
        self.data = {Table.CONTENT: App.RESOURCE_MANAGER.read(Table.CONTENT_PATH)}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def update(self, key, value, updater):
        self[key] = updater(self[key], value)

    def save(self, key, path):
        App.RESOURCE_MANAGER.write(self[key], path)


class Menu:
    def __init__(self, tk, name):
        self.tk = tk
        self.data = App.RESOURCE_MANAGER[name]
        self.frame = App.WIDGET_MANAGER.place_frame(self.tk, self.data['frame'])


class VisualizableMenu(Menu):
    def __init__(self, tk, name):
        super().__init__(tk, name)
        self.hidden = False
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


class MainMenu(VisualizableMenu):
    DATA_PATH = 'res/main_menu.yaml'

    def __init__(self, tk):
        super().__init__(tk, MainMenu)
        self.active = True
        self.buttons = self.prepare_buttons(self.data['buttons'])
        self.info_menu = None
        self.help_menu = None

    def prepare_buttons(self, data):
        return (
            App.WIDGET_MANAGER.pack_button(self.frame, data['play_button'], self.__play),
            App.WIDGET_MANAGER.pack_button(self.frame, data['info_button'], self.__info),
            App.WIDGET_MANAGER.pack_button(self.frame, data['help_button'], self.__help),
            App.WIDGET_MANAGER.pack_button(self.frame, data['exit_button'], self.__exit)
        )

    def __play(self):
        self.hide()
        Game(self).play()

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
        App.CACHE.save(Table.CONTENT, Table.CONTENT_PATH)
        self.active = False


class Game:
    DATA_PATH = 'res/game.yaml'

    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.tk = self.main_menu.tk
        data = App.RESOURCE_MANAGER[Game]
        self.canvas = App.WIDGET_MANAGER.pack_canvas(self.tk, data['canvas'])
        self.session = Session()
        self.paddle = Paddle(self.canvas, data['paddle'])
        self.ball = Ball(self.canvas, data['ball'], self.paddle)
        self.score = Score(self.canvas, data['score'])
        self.delay = data['delay']

    def play(self):
        # while self.ball.flies():
        #     self.ball.motion()
        #     self.tk.update_idletasks()
        #     self.tk.update()
        #     sleep(self.delay)
        self.canvas.pack_forget()
        self.session.finish()
        # self.main_menu.visualize()
        SummaryMenu(self.main_menu, self.session)


class Session:
    START = 'start'
    DURATION = 'duration'

    def __init__(self):
        self.data = {Session.START: str(time())}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def finish(self):
        self[Session.DURATION] = self.duration()

    def duration(self):
        return strftime('%H:%M:%S', gmtime(time() - float(self[Session.START])))


class Entity:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = None

    def prepare_rectangle(self, data):
        _id = self.canvas.create_rectangle(
            data['x1'], data['y1'], data['x2'], data['y2'], App.RESOURCE_MANAGER[ResourceManager.STYLES][data['style']]
        )
        self.canvas.move(_id, data['x0'], data['y0'])
        return _id

    def prepare_oval(self, data):
        _id = self.canvas.create_oval(
            data['x1'], data['y1'], data['x2'], data['y2'], App.RESOURCE_MANAGER[ResourceManager.STYLES][data['style']]
        )
        self.canvas.move(_id, data['x0'], data['y0'])
        return _id

    def prepare_text(self, data):
        _id = self.canvas.create_text(
            data['x1'], data['y1'], text=data['value'], font=App.RESOURCE_MANAGER[ResourceManager.FONTS][data['font']]
        )
        self.canvas.itemconfigure(_id, App.RESOURCE_MANAGER[ResourceManager.STYLES][data['style']])
        return _id

    def coordinates(self):
        return self.canvas.coords(self.id)


class MovableEntity(Entity):
    def __init__(self, canvas):
        super().__init__(canvas)

    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)


class Paddle(MovableEntity):
    def __init__(self, canvas, data):
        super().__init__(canvas)
        self.id = self.prepare_rectangle(data['rectangle'])
        self.dxl = data['dxl']
        self.dxr = data['dxr']
        self.canvas.bind_all(data['left_arrow'], self.__move_left)
        self.canvas.bind_all(data['right_arrow'], self.__move_right)

    # noinspection PyUnusedLocal
    def __move_left(self, event):
        self.move(self.dxl if self.hit_left_border() else 0, 0)

    def hit_left_border(self):
        return self.canvas.coords(self.id)[0] > 0

    # noinspection PyUnusedLocal
    def __move_right(self, event):
        self.move(self.dxr if self.hit_right_border() else 0, 0)

    def hit_right_border(self):
        return self.canvas.coords(self.id)[2] < self.canvas.winfo_width()


class Ball(MovableEntity):
    def __init__(self, canvas, data, paddle):
        super().__init__(canvas)
        self.id = self.prepare_oval(data['oval'])
        self.paddle = paddle
        self.dx = choice(data['dx'])
        self.dy = choice(data['dy'])
        self.dt = data['dt']

    def flies(self):
        return self.canvas.coords(self.id)[1] <= self.canvas.winfo_height()

    def motion(self):
        coordinates = self.coordinates()
        self.dx = self.move_x(coordinates)
        self.dy = self.move_y(coordinates)
        self.move(self.dx, self.dy)

    def move_x(self, coordinates):
        return 1 if self.hit_left_border(coordinates) else -1 if self.hit_right_border(coordinates) else self.dx

    # noinspection PyMethodMayBeStatic
    def hit_left_border(self, coordinates):
        return coordinates[0] <= 0

    def hit_right_border(self, coordinates):
        return coordinates[2] >= self.canvas.winfo_width()

    def move_y(self, coordinates):
        return 1 if self.hit_top_border(coordinates) else -1 if self.hit_paddle(coordinates) else self.dy

    # noinspection PyMethodMayBeStatic
    def hit_top_border(self, coordinates):
        return coordinates[1] <= 0

    def hit_paddle(self, coordinates):
        paddle_coordinates = self.paddle.coordinates()
        return self.upon_paddle(coordinates, paddle_coordinates) and self.touch_paddle(coordinates, paddle_coordinates)

    # noinspection PyMethodMayBeStatic
    def upon_paddle(self, coordinates, paddle_coordinates):
        return coordinates[2] >= paddle_coordinates[0] and coordinates[0] <= paddle_coordinates[2]

    # noinspection PyMethodMayBeStatic
    def touch_paddle(self, coordinates, paddle_coordinates):
        return paddle_coordinates[1] <= coordinates[3] <= paddle_coordinates[3]


class Score(Entity):
    def __init__(self, canvas, data):
        super().__init__(canvas)
        self.id = self.prepare_text(data['text'])
        self.value = data['text']['value']

    def increment(self):
        self.value += 1
        self.canvas.itemconfigure(self.id, text=str(self.value))


class SummaryMenu(Menu):
    DATA_PATH = 'res/summary_menu.yaml'

    def __init__(self, main_menu, session):
        super().__init__(main_menu.tk, SummaryMenu)
        self.main_menu = main_menu
        self.session = session
        # put table here
        self.ok_button = App.WIDGET_MANAGER.pack_button(self.frame, self.data['ok_button'], self.__ok)

    def __ok(self):
        self.frame.place_forget()
        # transmit session statistics to cache
        self.main_menu.visualize()

    # noinspection PyMethodMayBeStatic
    def __appender(self, lst, value):
        lst.append(value)
        return lst


class InfoMenu(VisualizableMenu):
    DATA_PATH = 'res/info_menu.yaml'

    def __init__(self, main_menu):
        super().__init__(main_menu.tk, InfoMenu)
        self.main_menu = main_menu
        self.table = Table(self, self.data['table'])
        self.back_button = App.WIDGET_MANAGER.pack_button(self.frame, self.data['back_button'], self.__back)

    def __back(self):
        self.hide()
        self.main_menu.visualize()

    def update(self):
        self.table.update()


class Table:
    CONTENT = 'content'
    CONTENT_PATH = 'res/table.yaml'

    def __init__(self, info_menu, data):
        self.info_menu = info_menu
        self.rows = data['rows']
        self.header_label = App.WIDGET_MANAGER.pack_label(self.info_menu.frame, data['header_label'])
        self.carcass = self.prepare_carcass(data['separator'], data['name_label'], data['result_label'])
        self.update()

    # noinspection PyUnusedLocal
    def prepare_carcass(self, separator_data, name_label_data, result_label_data):
        return [{
            'separator': App.WIDGET_MANAGER.pack_separator(self.info_menu.frame, separator_data),
            'name_label': App.WIDGET_MANAGER.pack_label(self.info_menu.frame, name_label_data),
            'result_label': App.WIDGET_MANAGER.pack_label(self.info_menu.frame, result_label_data)
        } for i in range(self.rows)]

    def update(self):
        content = self.limit(App.CACHE[Table.CONTENT])
        self.fill(content)
        App.CACHE[Table.CONTENT] = content

    def fill(self, content):
        for i in range(self.rows):
            self.carcass[i]['name_label'].configure(text=content[i]['name'])
            self.carcass[i]['result_label'].configure(text=content[i]['result'])

    def limit(self, content):
        return sorted(content, key=lambda r: r['result'], reverse=True)[:self.rows]


class HelpMenu(VisualizableMenu):
    DATA_PATH = 'res/help_menu.yaml'

    def __init__(self, main_menu):
        super().__init__(main_menu.tk, HelpMenu)
        self.main_menu = main_menu
        self.header_label = App.WIDGET_MANAGER.pack_label(self.frame, self.data['header_label'])
        self.wrapper_label = App.WIDGET_MANAGER.pack_label(self.frame, self.data['wrapper_label'])
        self.back_button = App.WIDGET_MANAGER.pack_button(self.frame, self.data['back_button'], self.__back)

    def __back(self):
        self.hide()
        self.main_menu.visualize()


if __name__ == '__main__':
    App().start()

from time import sleep
from tkinter import *
# from tkinter.ttk import Separator
from yaml import load, dump


class App:
    DATA_PATH = 'res/app.yaml'

    def __init__(self):
        self.rm = RM()
        data = self.rm[App]
        self.tk = self.prepare_tk(data['tk'])
        self.delay = data['delay']
        self.main_menu = MainMenu(self.rm, self.tk)

    # noinspection PyMethodMayBeStatic
    def prepare_tk(self, data):
        tk = Tk()
        tk.title(data['title'])
        tk.geometry('{}x{}'.format(tk.winfo_screenwidth(), tk.winfo_screenheight()))
        tk.resizable(data['resizable']['width'], data['resizable']['height'])
        tk.wm_attributes(data['wm_attributes'][0], data['wm_attributes'][1])
        tk.configure(background=data['background'])
        return tk

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
            RM.FONTS: load_data('res/fonts.yaml'), RM.STYLES: load_data('res/styles.yaml'),
            RM.POSITIONS: load_data('res/positions.yaml'), App: load_data(App.DATA_PATH),
            MainMenu: load_data(MainMenu.DATA_PATH), InfoMenu: load_data(InfoMenu.DATA_PATH),
            HelpMenu: load_data(HelpMenu.DATA_PATH)
        }

    def __getitem__(self, res):
        return self.data[res]


def load_data(path):
    with open(path) as stream:
        return load(stream)


class Menu:
    def __init__(self, rm, tk):
        self.rm = rm
        self.tk = tk
        self.hidden = False
        self.frame = None
        self.frame_place_info = None

    def prepare_frame(self, data):
        frame = Frame(self.tk, self.rm[RM.STYLES][data['style']])
        frame.place(self.rm[RM.POSITIONS][data['position']])
        frame.update()
        return frame

    def prepare_button(self, data, command):
        button = Button(self.frame, self.rm[RM.STYLES][data['style']])
        button.configure(text=data['text'], font=self.rm[RM.FONTS][data['font']], command=command)
        button.pack(self.rm[RM.POSITIONS][data['position']])
        button.update()
        return button

    def prepare_label(self, data):
        label = Label(self.frame, self.rm[RM.STYLES][data['style']])
        label.configure(text=data['text'], font=self.rm[RM.FONTS][data['font']])
        label.pack(self.rm[RM.POSITIONS][data['position']])
        label.update()
        return label

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

    def __init__(self, rm, tk):
        super().__init__(rm, tk)
        data = self.rm[MainMenu]
        self.frame = self.prepare_frame(data['frame'])
        self.buttons = self.prepare_buttons(data)
        self.info_menu = None
        self.help_menu = None
        self.active = True

    def prepare_buttons(self, data):
        return (
            self.prepare_button(data['play_button'], self.__play),
            self.prepare_button(data['info_button'], self.__info),
            self.prepare_button(data['help_button'], self.__help),
            self.prepare_button(data['exit_button'], self.__exit)
        )

    def __play(self):
        pass

    def __info(self):
        if self.info_menu is None:
            self.info_menu = InfoMenu(self.rm, self.tk, self)
        self.hide()
        self.info_menu.visualize()

    def __help(self):
        if self.help_menu is None:
            self.help_menu = HelpMenu(self.rm, self.tk, self)
        self.hide()
        self.help_menu.visualize()

    def __exit(self):
        if self.info_menu is not None:
            dump_data(self.info_menu.table_data, InfoMenu.TABLE_DATA_PATH)
        self.active = False


class InfoMenu(Menu):
    DATA_PATH = 'res/info_menu.yaml'
    TABLE_DATA_PATH = 'res/table.yaml'

    def __init__(self, rm, tk, main_menu):
        super().__init__(rm, tk)
        data = self.rm[InfoMenu]
        self.table_data = load_data(InfoMenu.TABLE_DATA_PATH)
        self.frame = self.prepare_frame(data['frame'])

        self.back_button = self.prepare_button(data['back_button'], self.__back)
        self.main_menu = main_menu

    def prepare_table(self, data):
        pass

    def __back(self):
        self.hide()
        self.main_menu.visualize()


def dump_data(data, path):
    with open(path, 'w') as stream:
        dump(data, stream, default_flow_style=False)


class HelpMenu(Menu):
    DATA_PATH = 'res/help_menu.yaml'

    def __init__(self, rm, tk, main_menu):
        super().__init__(rm, tk)
        data = self.rm[HelpMenu]
        self.frame = self.prepare_frame(data['frame'])
        self.header_label = self.prepare_label(data['header_label'])
        self.wrapper_label = self.prepare_label(data['wrapper_label'])
        self.back_button = self.prepare_button(data['back_button'], self.__back)
        self.main_menu = main_menu

    def __back(self):
        self.hide()
        self.main_menu.visualize()


# class Game:
#     """
#     All game processes occur at this class; session data is stored here as well.
#     The game is 2D, that's why there's an (xOy) coordinate system.
#     The beginning O(0, 0) is situated at the top left corner of the canvas, so Y axis is directed downwards, and X
#     axis is directed rightwards.
#     That's why if object's <dx> (horizontal shift) > 0, it moves rightwards; if <dx> < 0, it moves leftwards;
#     if <dy> (vertical shift) > 0, object moves downwards; if <dy> < 0, it moves upwards.
#     """
#     def __init__(self, data, canvas):
#         self.data = data
#         self.canvas = canvas
#         self.active = True
#         self.paddle = Paddle(canvas, self.data[PADDLE])
#         self.ball = Ball(canvas, self.data[BALL], self.paddle.id)
#
#     def __prepare_canvas(self):
#         data = self.data[CANVAS]
#         canvas = Canvas(self.tk, width=data[WIDTH], height=data[HEIGHT], bg=data[BG],
#                         bd=data[BD], highlightthickness=data[HIGHLIGHTTHICKNESS])
#         canvas.pack()
#         canvas.update()
#         return canvas
#
#     def active(self):
#         return self.active
#
#
# class Paddle:
#     """
#     Paddle object class, order by the player.
#     Use left and right arrows to move this stuff and hit the ball.
#
#         canvas:  TKinter's object, where paddle's rectangle is created and moved.
#         id:  paddle's id in the list of canvas' objects
#         dxl:  paddle's left movement in pixels per 1 tact
#         dxr:  paddle's right movement in pixels per 1 tact
#     """
#     def __init__(self, canvas, data):
#         self.canvas = canvas
#         self.id = self.canvas.create_rectangle(data[X1], data[Y1], data[X2], data[Y2], fill=data[FILL])
#         self.dxl = data[DXL]
#         self.dxr = data[DXR]
#         self.canvas.move(self.id, data[X0], data[Y0])
#         self.canvas.bind_all(data[LEFT_ARROW], self.__move_left)
#         self.canvas.bind_all(data[RIGHT_ARROW], self.__move_right)
#
#     # noinspection PyUnusedLocal
#     def __move_left(self, event):
#         """
#         Moves the paddle by <dxl> pixes leftwards.
#         """
#         self.canvas.move(self.id, self.dxl if self.canvas.coords(self.id)[0] > 0 else 0, 0)
#
#     # noinspection PyUnusedLocal
#     def __move_right(self, event):
#         """
#         Moves the paddle by <dxr> pixels rightwards.
#         """
#         self.canvas.move(self.id, self.dxr if self.canvas.coords(self.id)[2] < self.canvas.winfo_width() else 0, 0)
#
#
# class Ball:
#     """
#     The main game's flywheel, which forces the player to hit it.
#     It's a round itself, which has a speed vector, defined by <dx> and <dy> coordinates; after each hit the ball
#     has a little acceleration according to the physical principles.
#     If it overcomes the canvas' bottom, the player loses.
#
#         canvas:  TKinter's object, where ball's wheel is created.
#         canvas_width:  canvas width in pixels
#         canvas_height: canvas height in pixels
#         id:  ball's id in the list of canvas' objects
#         paddle_id:  paddle's id  used for hit calculation
#         dx:  horizontal shift in pixels per 1 tact
#         dy:  vertical shift in pixels per 1 tact
#     """
#     def __init__(self, canvas, data, paddle_id):
#         self.canvas = canvas
#         self.canvas_width = self.canvas.winfo_width()
#         self.canvas_height = self.canvas.winfo_height()
#         self.id = self.canvas.create_oval(data[X1], data[Y1], data[X2], data[Y2], fill=data[FILL])
#         self.paddle_id = paddle_id
#         self.dx = choice(data[DX])
#         self.dy = choice(data[DY])
#         self.canvas.move(self.id, data[X0], data[Y0])
#
#     def move(self):
#         """
#         Moves the ball on the canvas via the speed vector {<dx>, <dy>}.
#         """
#         coords = self.canvas.coords(self.id)
#         self.dx = 1 if self.__hit_left_border(coords) else -1 if self.__hit_right_border(coords) else self.dx
#         self.dy = 1 if self.__hit_top_border(coords) else -1 if self.__hit_paddle(coords) else self.dy
#         self.canvas.move(self.id, self.dx, self.dy)
#
#     def flies(self):
#         """
#         Checks if the ball has overcome the canvas' bottom.
#         """
#         return self.canvas.coords(self.id)[1] <= self.canvas_height
#
#     # noinspection PyMethodMayBeStatic
#     def __hit_left_border(self, coords):
#         """
#         Checks if the ball hits the canvas' left border.
#         """
#         return coords[0] <= 0
#
#     def __hit_right_border(self, coords):
#         """
#         Checks if the ball hits the canvas' right border.
#         """
#         return coords[2] >= self.canvas_width
#
#     # noinspection PyMethodMayBeStatic
#     def __hit_top_border(self, coords):
#         """
#         Checks if the ball hits the canvas' top border.
#         """
#         return coords[1] <= 0
#
#     def __hit_paddle(self, coords):
#         """
#         Checks if the ball hits the paddle.
#         """
#         paddle_coords = self.canvas.coords(self.paddle_id)
#         return paddle_coords[1] <= coords[3] <= paddle_coords[3] and \
#             coords[2] >= paddle_coords[0] and coords[0] <= paddle_coords[2]
#


if __name__ == '__main__':
    App().start()

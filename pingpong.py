from time import sleep
from tkinter import *
from tkinter.font import Font
from yaml import load


class App:
    DATA_PATH = 'res/app.yaml'

    def __init__(self):
        self.rm = RM()
        self.data = self.rm[App]
        self.tk = self.prepare_tk(self.data['tk'])
        self.delay = self.data['delay']
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
            RM.FONTS: self.load_data('res/fonts.yaml'), RM.STYLES: self.load_data('res/styles.yaml'),
            RM.POSITIONS: self.load_data('res/positions.yaml'), App: self.load_data(App.DATA_PATH),
            MainMenu: self.load_data(MainMenu.DATA_PATH), HelpMenu: self.load_data(HelpMenu.DATA_PATH)
        }
        self.data = {key: self.prepare_data(value) for key, value in self.data.items()}

    # noinspection PyMethodMayBeStatic
    def load_data(self, path):
        with open(path) as stream:
            return load(stream)

    def prepare_data(self, data):
        prepared_data = {}
        # print(self.data[RM.FONTS]['button_font'])
        for key1, value1 in data.items():
            if type(data[key1]) is dict:
                prepared_data[key1] = {}
                for key2, value2 in value1.items():
                    prepared_data[key1][key2] = self.bind(key2, value2)
            else:
                prepared_data[key1] = value1
        return prepared_data

    # noinspection PyMethodMayBeStatic
    def bind(self, key, value):
        if key == 'font':
            return Font(self.data[RM.FONTS][value])
        elif key == 'style':
            return self[RM.STYLES][value]
        elif key == 'position':
            return self[RM.POSITIONS][value]
        return value

    def __getitem__(self, key):
        return self.data[key]


class Menu:
    def __init__(self, rm, tk):
        self.rm = rm
        self.data = None
        self.tk = tk
        self.hidden = False
        self.frame = None
        self.frame_place_info = None

    def prepare_frame(self, data):
        frame = Frame(self.tk, data['style'])
        frame.place(data['position'])
        frame.update()
        return frame

    def prepare_button(self, data, command):
        button = Button(self.frame, data['style'])
        button.configure(text=data['text'], command=command)
        button.pack(data['position'])
        button.update()
        return button

    def prepare_label(self, data):
        label = Label(self.frame, data['style'])
        label.configure(text=data['text'])
        label.pack()
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
        self.data = self.rm[MainMenu]
        self.frame = self.prepare_frame(self.data['frame'])
        self.buttons = (
            self.prepare_button(self.data['play_button'], self.__play),
            self.prepare_button(self.data['info_button'], self.__info),
            self.prepare_button(self.data['help_button'], self.__help),
            self.prepare_button(self.data['exit_button'], self.__exit)
        )
        self.help_menu = None
        self.active = True

    def __play(self):
        pass

    def __info(self):
        pass

    def __help(self):
        self.help_menu = self.check_help_menu()
        self.hide()
        self.help_menu.visualize()

    def check_help_menu(self):
        return HelpMenu(self.rm, self.tk, self) if self.help_menu is None else self.help_menu

    def __exit(self):
        self.active = False


class HelpMenu(Menu):
    DATA_PATH = 'res/help_menu.yaml'

    def __init__(self, rm, tk, main_menu):
        super().__init__(rm, tk)
        self.data = self.rm[HelpMenu]
        self.frame = self.prepare_frame(self.data['frame'])
        self.header_label = self.prepare_label(self.data['header_label'])
        self.wrapper_label = self.prepare_label(self.data['wrapper_label'])
        self.back_button = self.prepare_button(self.data['back_button'], self.__back)
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

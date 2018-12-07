from globals import RM, Screen
from random import choice, uniform
from time import sleep, time, strftime, gmtime
from factory import pack_canvas, create_rectangle, create_oval, create_text, create_line


class Game(Screen):
    def __init__(self, main_menu):
        super().__init__(main_menu.tk, RM.GAME)
        self.canvas = pack_canvas(self.tk, self.data['canvas'])
        self.paddle = Paddle(self.canvas, self.data['paddle'])
        self.ball = Ball(self.canvas, self.data['ball'], self.paddle)
        self.score = Score(self.canvas, self.data['score'])
        self.session = Session()
        self.delay = self.data['delay']

    def play(self):
        while self.ball.flies():
            self.ball.motion()
            self.tk.update_idletasks()
            self.tk.update()
            sleep(self.delay)
        self.canvas.pack_forget()
        self.session.finish()
        return self.session


class Entity:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = None

    def coordinates(self):
        return self.canvas.coords(self.id)


class MovableEntity(Entity):
    def __init__(self, canvas):
        super().__init__(canvas)

    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)


class Decoration(MovableEntity):
    def __init__(self, canvas, data):
        super().__init__(canvas)
        self.id = create_line(self.canvas, data['line'])


class Paddle(MovableEntity):
    def __init__(self, canvas, data):
        super().__init__(canvas)
        self.id = create_rectangle(self.canvas, data['rectangle'])
        self.vxl = data['vx']
        self.vxr = -self.vxl
        self.canvas.bind_all(data['left_arrow'], self.__move_left)
        self.canvas.bind_all(data['right_arrow'], self.__move_right)

    # noinspection PyUnusedLocal
    def __move_left(self, event):
        self.move(self.vxl if self.hit_left_border() else 0, 0)

    def hit_left_border(self):
        return self.canvas.coords(self.id)[0] > 0

    # noinspection PyUnusedLocal
    def __move_right(self, event):
        self.move(self.vxr if self.hit_right_border() else 0, 0)

    def hit_right_border(self):
        return self.canvas.coords(self.id)[2] < self.canvas.winfo_width()


# noinspection PyMethodMayBeStatic
class Ball(MovableEntity):
    def __init__(self, canvas, data, paddle):
        super().__init__(canvas)
        self.id = create_oval(self.canvas, data['oval'])
        self.paddle = paddle
        self.vx = self.calc_vx0(data['vx_range'])
        self.vx_random = data['vx_random']
        self.vy = self.calc_vy0(data['vy_range'])
        self.dvy = data['g'] * data['dt']

    def calc_vx0(self, data):
        return choice([uniform(data[0], data[1]), uniform(-data[1], -data[0])])

    def calc_vy0(self, data):
        return uniform(data[0], data[1])

    def flies(self):
        return self.canvas.coords(self.id)[1] <= self.canvas.winfo_height()

    def motion(self):
        coordinates = self.coordinates()
        self.vx = self.calc_vx(coordinates)
        self.vy = self.calc_vy(coordinates)
        self.move(self.vx, self.vy)

    def calc_vx(self, coordinates):
        return -self.vx * self.calc_vx_random() if self.hit_vertical_borders(coordinates) else self.vx

    def calc_vx_random(self):
        return 1 + uniform(-self.vx_random, self.vx_random)

    def hit_vertical_borders(self, coordinates):
        return self.hit_left_border(coordinates) or self.hit_right_border(coordinates)

    def hit_left_border(self, coordinates):
        return coordinates[0] <= 0

    def hit_right_border(self, coordinates):
        return coordinates[2] >= self.canvas.winfo_width()

    def calc_vy(self, coordinates):
        return (-self.vy if self.hit_horizontal_borders(coordinates) else self.vy) + self.dvy

    def hit_horizontal_borders(self, coordinates):
        return self.hit_top_border(coordinates) or self.hit_paddle(coordinates)

    def hit_top_border(self, coordinates):
        return coordinates[1] <= 0

    def hit_paddle(self, coordinates):
        paddle_coordinates = self.paddle.coordinates()
        return self.upon_paddle(coordinates, paddle_coordinates) and self.touch_paddle(coordinates, paddle_coordinates)

    def upon_paddle(self, coordinates, paddle_coordinates):
        return coordinates[2] >= paddle_coordinates[0] and coordinates[0] <= paddle_coordinates[2]

    def touch_paddle(self, coordinates, paddle_coordinates):
        return paddle_coordinates[1] <= coordinates[3] <= paddle_coordinates[3]


class Score(Entity):
    def __init__(self, canvas, data):
        super().__init__(canvas)
        self.id = create_text(self.canvas, data['text'])
        self.value = data['text']['value']

    def increment(self):
        self.value += 1
        self.canvas.itemconfigure(self.id, text=str(self.value))


class Session:
    DURATION = 'duration'
    SCORE = 'score'

    def __init__(self):
        self.data = {Session.SCORE: 0}
        self.start = time()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def finish(self):
        self[Session.DURATION] = strftime('%H:%M:%S', gmtime(time() - self.start))

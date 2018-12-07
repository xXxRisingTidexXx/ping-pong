from globals import RM, Screen
from random import choice
from time import sleep, time, strftime, gmtime
from factory import pack_canvas, generate_rectangle, generate_oval, generate_text


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


class Paddle(MovableEntity):
    def __init__(self, canvas, data):
        super().__init__(canvas)
        self.id = generate_rectangle(self.canvas, data['rectangle'])
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
        self.id = generate_oval(self.canvas, data['oval'])
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
        self.id = generate_text(self.canvas, data['text'])
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

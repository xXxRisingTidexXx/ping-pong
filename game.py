# noinspection PyUnresolvedReferences
from math import cos, sin, pi, sqrt
from globals import RM, Screen
from random import choice, uniform
from time import sleep, time, strftime, gmtime
from factory import pack_canvas, create_rectangle, create_oval, create_text, create_line


class Game(Screen):
    def __init__(self, main_menu):
        super().__init__(main_menu.tk, RM.GAME)
        self.canvas = pack_canvas(self.tk, self.data['canvas'])
        self.decorations = self.prepare_decorations(self.data['decorations'])
        self.paddle = Paddle(self.canvas, self.data['paddle'])
        self.ball = Ball(self.canvas, self.data['ball'], self.paddle)
        self.score = Score(self.canvas, self.data['score'])
        self.target_generator = TargetGenerator(self.canvas, self.data['target'])
        self.target_collector = TargetCollector(self.canvas)
        self.session = Session()
        self.delay = self.data['delay']

    def prepare_decorations(self, data):
        return [Decoration(self.canvas, d) for d in data]

    def play(self):
        self.mainloop()
        self.finish()
        return self.session

    def mainloop(self):
        while self.ball.flies():
            self.generate_targets()
            self.ball.motion()
            self.check_targets()
            self.motion_decorations()
            self.tk.update_idletasks()
            self.tk.update()
            sleep(self.delay)

    def generate_targets(self):
        self.target_collector.extend(self.target_generator.try_generate())

    def check_targets(self):
        targets = self.ball.find_targets()
        count = len(targets)
        if count > 0:
            self.score.increase(count)
            self.session[Session.SCORE] = self.score.value
            self.target_collector.remove(targets)

    def motion_decorations(self):
        for d in self.decorations:
            d.motion()

    def finish(self):
        self.canvas.pack_forget()
        self.session.finish()


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
        self.vx0 = data['vx0']
        self.xmover = eval(data['xmover'])
        self.vy0 = data['vy0']
        self.ymover = eval(data['ymover'])
        self.w = data['w']

    def motion(self):
        self.move(self.xmover(self.vx0, self.w), self.ymover(self.vy0, self.w))


# noinspection PyUnusedLocal
class Paddle(MovableEntity):
    def __init__(self, canvas, data):
        super().__init__(canvas)
        self.id = create_rectangle(self.canvas, data['rectangle'])
        self.vxl = data['vx']
        self.vxr = -self.vxl
        self.canvas.bind_all(data['left_arrow'], self.__move_left)
        self.canvas.bind_all(data['right_arrow'], self.__move_right)

    def __move_left(self, event):
        self.move(self.vxl if self.hit_left_border() else 0, 0)

    def hit_left_border(self):
        return self.canvas.coords(self.id)[0] > 0

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
        self.r = self.calc_r(data['oval'])
        self.vx = self.calc_vx0(data['vx_range'])
        self.vx_random = data['vx_random']
        self.vy = self.calc_vy0(data['vy_range'])
        self.dvy = data['g'] * data['dt']

    def calc_r(self, data):
        return abs(data['x1'] - data['x2']) / 2

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

    def find_targets(self):
        return tuple(filter(lambda t: 'target' in self.canvas.gettags(t), self.find_overlapping()))

    def find_overlapping(self):
        coordinates = self.coordinates()
        shift = self.calc_shift()
        return self.canvas.find_overlapping(
            coordinates[0] + shift, coordinates[1] + shift, coordinates[2] - shift, coordinates[3] - shift
        )

    def calc_shift(self):
        return self.r * (1 - sqrt(0.5))


class Score(Entity):
    def __init__(self, canvas, data):
        super().__init__(canvas)
        self.id = create_text(self.canvas, data['text'])
        self.value = data['text']['value']

    def increase(self, increasing):
        self.value += increasing
        self.canvas.itemconfigure(self.id, text=str(self.value))


class TargetGenerator:
    def __init__(self, canvas, target_data):
        self.canvas = canvas
        self.target_data = target_data
        self.start = time()

    # I'm too lazy to change it :) Later we will modify it)
    def try_generate(self):
        now = time()
        targets = []
        if now - self.start >= 10:
            self.start = now
            targets.append(Target(self.canvas, self.target_data, uniform(50, 1300), uniform(50, 500)))
        return targets


class Target(Entity):
    def __init__(self, canvas, data, x, y):
        super().__init__(canvas)
        self.id = self.prepare_rectangle(data['rectangle'], x, y)

    def prepare_rectangle(self, data, x, y):
        _id = create_rectangle(self.canvas, data)
        self.canvas.move(_id, x, y)
        self.canvas.itemconfigure(_id, tag='target')
        return _id


class TargetCollector:
    def __init__(self, canvas):
        self.canvas = canvas
        self.targets = []

    def extend(self, targets):
        if len(targets) > 0:
            self.targets.extend(targets)

    def remove(self, targets):
        self.targets = list(filter(lambda i: i not in targets, self.targets))
        for t in targets:
            self.canvas.delete(t)


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

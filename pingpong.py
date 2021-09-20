from tkinter import Tk, Frame, Button, Label, Canvas, Event, Widget
from typing import Callable
from random import choice, uniform


def main():
    tk = Tk()
    tk.wm_title('ping-pong')
    tk.wm_geometry(f'{tk.winfo_screenwidth()}x{tk.winfo_screenheight()}')
    tk.wm_resizable(0, 0)
    # tk.wm_attributes('-topmost', 1, '-type', 'splash')
    tk.configure(background=Color.background)
    make_menu(tk)
    tk.mainloop()


class Color:
    background = '#000000'
    accent = '#c868db'
    hover = '#ffffff'
    button_text = '#000000'
    label_text = '#bca3d6'
    paddle = '#e8e3d9'
    ball = '#c7dbf4'


class Font:
    button = ('Consolas', 18, 'bold')
    header = ('Consolas', 22, 'bold')
    paragraph = ('Consolas', 14, 'normal')


def make_menu(tk: Tk):
    frame = Frame(
        tk,
        highlightthickness=2,
        bg=Color.background,
        highlightbackground=Color.accent,
        padx=5,
        pady=10
    )
    frame.place_configure(relx=0.5, rely=0.5, anchor='center')
    options = [
        ('Play', go_to_scene(make_game, tk, frame)),
        ('Help', go_to_scene(make_help, tk, frame)),
        ('Quit', tk.quit)
    ]
    for text, command in options:
        button = Button(
            frame,
            relief='flat',
            highlightthickness=0,
            bg=Color.accent,
            fg=Color.button_text,
            activebackground=Color.hover,
            activeforeground=Color.button_text,
            text=text,
            font=Font.button,
            command=command
        )
        button.pack_configure(padx=25, pady=18, ipadx=70, ipady=8, fill='x')


def make_game(tk: Tk):
    canvas_width, canvas_height = tk.winfo_width(), tk.winfo_height()
    canvas = Canvas(
        tk,
        width=canvas_width,
        height=canvas_height,
        highlightthickness=0,
        bg=Color.background
    )
    canvas.pack_configure(expand=True, fill='both')
    paddle_width, paddle_height = 150, 10
    paddle_x, paddle_y = (tk.winfo_width() - paddle_width) // 2, tk.winfo_height() - 300
    paddle_id = canvas.create_rectangle(
        paddle_x,
        paddle_y,
        paddle_x + paddle_width,
        paddle_y + paddle_height,
        width=0,
        fill=Color.paddle
    )
    paddle_vx = 6.5
    canvas.bind_all('<Key-Left>', move_paddle_left(canvas, paddle_id, paddle_vx))
    canvas.bind_all('<Key-Right>', move_paddle_right(canvas, paddle_id, paddle_vx))
    ball_x, ball_y, ball_r = 455, 300, 15
    ball_id = canvas.create_oval(
        ball_x,
        ball_y,
        ball_x + 2 * ball_r,
        ball_y + 2 * ball_r,
        width=0,
        fill=Color.ball
    )
    ball_vx, ball_vy = uniform(-2, -1), uniform(-3, -2)
    canvas.after(0, move_ball(canvas, ball_id, paddle_id, choice([ball_vx, -ball_vx]), ball_vy))


Handler = Callable[[Event], None]


def move_paddle_left(canvas: Canvas, id_: int, vx: float) -> Handler:
    def move(_: Event):
        dx = canvas.coords(id_)[0]
        if dx > 0:
            canvas.move(id_, -(vx if dx > vx else dx), 0)
    return move


def move_paddle_right(canvas: Canvas, id_: int, vx: float) -> Handler:
    def move(_: Event):
        dx = canvas.winfo_width() - canvas.coords(id_)[2]
        if dx > 0:
            canvas.move(id_, vx if dx > vx else dx, 0)
    return move


Callback = Callable[[], None]


def move_ball(canvas: Canvas, ball_id: int, paddle_id: int, vx: float, vy: float) -> Callback:
    delay = 10
    dvy = delay * 0.0012

    def move():
        ball_coords = canvas.coords(ball_id)
        vx1 = (
            -vx * (1 + uniform(-0.1, 0.1))
            if ball_coords[0] <= 0 or ball_coords[2] >= canvas.winfo_width()
            else vx
        )
        paddle_coords = canvas.coords(paddle_id)
        vy1 = dvy + (
            -vy
            if (
                ball_coords[1] <= 0 or
                ball_coords[2] >= paddle_coords[0] and
                ball_coords[0] <= paddle_coords[2] and
                paddle_coords[1] <= ball_coords[3] <= paddle_coords[3]
            )
            else vy
        )
        canvas.move(ball_id, vx1, vy1)
        canvas.after(delay, move_ball(canvas, ball_id, paddle_id, vx1, vy1))
    return move


def go_to_scene(scene: Callable[[Tk], None], tk: Tk, widget: Widget) -> Callback:
    def go_to():
        scene(tk)
        widget.destroy()
    return go_to


def make_help(tk: Tk):
    frame = Frame(tk, bg=Color.background, padx=10, pady=30)
    frame.place_configure(relx=0.5, rely=0.5, anchor='center')
    contents = [
        ('ping-pong', Font.header),
        (
            'It\'s a classic ping-pong game, where you\'re to hit the ball\n'
            'using the paddle. The more ball doesn\'t hit the floor, the\n'
            'more points you score. Use left and right arrows to move the\n'
            'paddle. Hit special targets to score extra points.',
            Font.paragraph
        )
    ]
    for text, font in contents:
        label = Label(
            frame,
            relief='flat',
            highlightthickness=0,
            bg=Color.background,
            fg=Color.label_text,
            text=text,
            font=font
        )
        label.pack_configure(padx=30, pady=10, ipadx=30, ipady=5)
    button = Button(
        frame,
        relief='flat',
        highlightthickness=0,
        bg=Color.accent,
        fg=Color.button_text,
        activebackground=Color.hover,
        activeforeground=Color.button_text,
        text='Back',
        font=Font.button,
        command=go_to_scene(make_menu, tk, frame)
    )
    button.pack_configure(padx=25, pady=20, ipadx=130, ipady=10)


if __name__ == '__main__':
    main()

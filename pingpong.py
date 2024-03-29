from tkinter import Tk, Frame, Button, Label, Canvas, Event
from typing import Callable
from random import uniform, choice
from pathlib import Path
from pygame.mixer import init, music

# Music voice levels for various scenes.
MENU_VOLUME = 0.45
GAME_VOLUME = 1

# Widget colors in hex format.
BACKGROUND_COLOR = '#000000'
ACCENT_COLOR = '#c868db'
HOVER_COLOR = '#ffffff'
BUTTON_TEXT_COLOR = '#000000'
LABEL_TEXT_COLOR = '#bca3d6'
SPRITE_COLOR = '#e8e3d9'

# Text formats.
BUTTON_FONT = ('Consolas', 18, 'bold')
HEADER_FONT = ('Consolas', 22, 'bold')
PARAGRAPH_FONT = ('Consolas', 14, 'normal')
SCORE_FONT = ('Consolas', 50, 'bold')

# Unique keyboard button identifiers.
KEY_LEFT = '<Key-Left>'
KEY_RIGHT = '<Key-Right>'

# Environment Tcl/Tk variable names.
GAME_IS_RUNNING = 'PINGPONG_GAME_IS_RUNNING'
BALL_IS_MOVING = 'PINGPONG_BALL_IS_MOVING'


def main():
    """
    This is the game entrypoint. Here tkinter and pygame are ste up. Desktop window size, required
    widgets, music player and so on are configured here.
    """
    tk = Tk()
    tk.wm_title('ping-pong')
    tk.wm_geometry(f'{tk.winfo_screenwidth()}x{tk.winfo_screenheight()}')
    tk.wm_resizable(0, 0)
    tk.wm_attributes('-topmost', 1, '-type', 'splash')
    tk.configure(background=BACKGROUND_COLOR)
    init()
    music.load(Path('assets') / 'ambience.ogg')
    music.set_volume(MENU_VOLUME)
    music.play(-1)
    make_menu(tk)
    tk.mainloop()


def make_menu(tk: Tk):
    """
    It's a selection activity constructor. It creates required widgets. WHat's more, it binds
    option buttons to transitions to other scenes and to the host OS.
    """
    frame = Frame(
        tk,
        highlightthickness=2,
        bg=BACKGROUND_COLOR,
        highlightbackground=ACCENT_COLOR,
        padx=5,
        pady=10
    )
    frame.place_configure(relx=0.5, rely=0.5, anchor='center')
    options = [
        ('Play', go_to_scene(make_game, tk, frame)),
        ('Help', go_to_scene(make_help, tk, frame)),
        ('Quit', quit_tk(tk))
    ]
    for text, command in options:
        button = Button(
            frame,
            relief='flat',
            highlightthickness=0,
            bg=ACCENT_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=BUTTON_TEXT_COLOR,
            text=text,
            font=BUTTON_FONT,
            command=command
        )
        button.pack_configure(padx=25, pady=18, ipadx=70, ipady=8, fill='x')


def make_game(tk: Tk):
    """
    The main activity constructor. It turns on the music volume to max level, allocates canvas and
    manages its entity motions. Generally speaking, there're just two sprites over here: the ball
    and the paddle. The first one is periodically re-rendered by the game, the last one's managed
    by the player. The endgame condition is the ball being fallen over the bottom viewport border.
    """
    music.set_volume(GAME_VOLUME)
    canvas_width, canvas_height = tk.winfo_width(), tk.winfo_height()
    canvas = Canvas(
        tk,
        width=canvas_width,
        height=canvas_height,
        highlightthickness=0,
        bg=BACKGROUND_COLOR
    )
    canvas.pack_configure(expand=True, fill='both')
    canvas.setvar(GAME_IS_RUNNING)
    canvas.setvar(BALL_IS_MOVING)
    canvas.update()
    paddle_width, paddle_height = 150, 10
    paddle_x, paddle_y = (canvas.winfo_width() - paddle_width) // 2, canvas.winfo_height() - 300
    paddle_id = canvas.create_rectangle(
        paddle_x,
        paddle_y,
        paddle_x + paddle_width,
        paddle_y + paddle_height,
        width=0,
        fill=SPRITE_COLOR
    )
    paddle_vx = 8
    canvas.bind_all(KEY_LEFT, move_paddle_left(canvas, paddle_id, paddle_vx))
    canvas.bind_all(KEY_RIGHT, move_paddle_right(canvas, paddle_id, paddle_vx))
    ball_x, ball_y, ball_r = 455, 300, 15
    ball_id = canvas.create_oval(
        ball_x,
        ball_y,
        ball_x + 2 * ball_r,
        ball_y + 2 * ball_r,
        width=0,
        fill=SPRITE_COLOR
    )
    ball_vx, ball_vy = uniform(-3, -1), uniform(-4, -2)
    delay = 10
    canvas.after(
        0,
        move_ball(canvas, ball_id, paddle_id, choice([ball_vx, -ball_vx]), ball_vy, delay)
    )
    canvas.after(0, check_fall(tk, canvas, ball_id, delay))


# A shortcut for functions managing tkinter phenomena.
Handler = Callable[[Event], None]


def move_paddle_left(canvas: Canvas, id_: int, vx: float) -> Handler:
    """
    A callback maker being used to move the paddle left if possible. It's called by the event
    'The user has pressed the left arrow button'.
    """
    def move(_: Event):
        dx = canvas.coords(id_)[0]
        if dx > 0:
            canvas.move(id_, -(vx if dx > vx else dx), 0)
    return move


def move_paddle_right(canvas: Canvas, id_: int, vx: float) -> Handler:
    """
    A callback maker being used to move the paddle right if possible. It's called by the event
    'The user has pressed the right arrow button'.
    """
    def move(_: Event):
        dx = canvas.winfo_width() - canvas.coords(id_)[2]
        if dx > 0:
            canvas.move(id_, vx if dx > vx else dx, 0)
    return move


# A shortcut for event handlers without tkinter event objects.
Callback = Callable[[], None]


def move_ball(
    canvas: Canvas,
    ball_id: int,
    paddle_id: int,
    vx: float,
    vy: float,
    delay: int
) -> Callback:
    """
    The overall game mechanics occurs here. The very first thing to mention is the implicit
    recursion of this logic. It move the ball periodically until it falls down. This's the
    principle of re-rendering. The second important thing is the ball speed calculation. It follows
    uniformly accelerated motion, that's why the ball is permanently "trying" to fall. And its
    reflections from the canvas sides and the paddle are calculated here as well.
    """
    def move():
        ball_coords = canvas.coords(ball_id)
        vx1 = (
            -vx * (1 + uniform(-0.1, 0.1))
            if ball_coords[0] <= 0 or ball_coords[2] >= canvas.winfo_width()
            else vx
        )
        paddle_coords = canvas.coords(paddle_id)
        vy1 = delay * 0.002 + (
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
        if canvas.getvar(GAME_IS_RUNNING) == '1':
            canvas.after(delay, move_ball(canvas, ball_id, paddle_id, vx1, vy1, delay))
        else:
            canvas.setvar(BALL_IS_MOVING, '0')
    return move


def check_fall(tk: Tk, canvas: Canvas, id_: int, delay: int) -> Callback:
    """
    This task periodically verifies whether the ball has crossed the bottom line. After that the
    job waits far other calculations to be finalized.
    """
    def check():
        if canvas.coords(id_)[1] <= canvas.winfo_height():
            canvas.after(delay, check)
        else:
            canvas.setvar(GAME_IS_RUNNING, '0')
            canvas.wait_variable(BALL_IS_MOVING)
            canvas.unbind_all(KEY_LEFT)
            canvas.unbind_all(KEY_RIGHT)
            music.set_volume(MENU_VOLUME)
            make_menu(tk)
            canvas.destroy()
    return check


def go_to_scene(scene: Callable[[Tk], None], tk: Tk, frame: Frame) -> Callback:
    """
    A useful shortcut for transition between the scenes.
    """
    def go_to():
        scene(tk)
        frame.destroy()
    return go_to


def make_help(tk: Tk):
    """
    Renders a helping message with a brief description of the game rules.
    """
    frame = Frame(tk, bg=BACKGROUND_COLOR, padx=10, pady=30)
    frame.place_configure(relx=0.5, rely=0.5, anchor='center')
    contents = [
        ('ping-pong', HEADER_FONT),
        (
            'It\'s a classic ping-pong game, where you\'re to hit the ball\n'
            'using the paddle. The more ball doesn\'t hit the floor, the\n'
            'more points you score. Use left and right arrows to move\n'
            'the paddle.',
            PARAGRAPH_FONT
        )
    ]
    for text, font in contents:
        label = Label(
            frame,
            relief='flat',
            highlightthickness=0,
            bg=BACKGROUND_COLOR,
            fg=LABEL_TEXT_COLOR,
            text=text,
            font=font
        )
        label.pack_configure(padx=30, pady=10, ipadx=30, ipady=5)
    button = Button(
        frame,
        relief='flat',
        highlightthickness=0,
        bg=ACCENT_COLOR,
        fg=BUTTON_TEXT_COLOR,
        activebackground=HOVER_COLOR,
        activeforeground=BUTTON_TEXT_COLOR,
        text='Back',
        font=BUTTON_FONT,
        command=go_to_scene(make_menu, tk, frame)
    )
    button.pack_configure(padx=25, pady=20, ipadx=130, ipady=10)


def quit_tk(tk: Tk) -> Callback:
    """
    Finalizes the application and exits to the host OS.
    """
    def finalize():
        music.stop()
        tk.quit()
    return finalize


if __name__ == '__main__':
    main()

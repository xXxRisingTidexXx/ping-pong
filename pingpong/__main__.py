from tkinter import Tk, Frame, Button, Label, Canvas, Event, Widget
from typing import Callable


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
        ('Play', _go_to_scene(make_game, tk, frame)),
        ('Help', _go_to_scene(make_help, tk, frame)),
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
    canvas = Canvas(
        tk,
        width=tk.winfo_width(),
        height=tk.winfo_height(),
        highlightthickness=0,
        bg=Color.background
    )
    canvas.pack_configure(expand=True, fill='both')
    paddle_width = 150
    paddle_id = canvas.create_rectangle(0, 0, paddle_width, 10, width=0, fill='#e8e3d9')
    canvas.move(paddle_id, (tk.winfo_width() - paddle_width) // 2, tk.winfo_height() - 300)
    paddle_vx = 6.5
    canvas.bind_all('<Key-Left>', _move_paddle_left(canvas, paddle_id, -paddle_vx))
    canvas.bind_all('<Key-Right>', _move_paddle_right(canvas, paddle_id, paddle_vx))


Handler = Callable[[Event], None]


def _move_paddle_left(canvas: Canvas, id_: int, vx: float) -> Handler:
    def move(_: Event):
        if canvas.coords(id_)[0] > 0:
            canvas.move(id_, vx, 0)
    return move


def _move_paddle_right(canvas: Canvas, id_: int, vx: float) -> Handler:
    def move(_: Event):
        dx = canvas.winfo_width() - canvas.coords(id_)[2]
        if dx > 0:
            canvas.move(id_, vx if dx > vx else dx, 0)
    return move


def _go_to_scene(scene: Callable[[Tk], None], tk: Tk, widget: Widget) -> Callable[[], None]:
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
        command=_go_to_scene(make_menu, tk, frame)
    )
    button.pack_configure(padx=25, pady=20, ipadx=130, ipady=10)


if __name__ == '__main__':
    main()

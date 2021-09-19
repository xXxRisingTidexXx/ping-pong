from tkinter import Tk, Frame, Button, Label
from typing import Callable
from pingpong.theme import Color, Font


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
    options = [('Help', _go_to_scene(make_help, tk, frame)), ('Quit', tk.quit)]
    for text, command in options:
        button = Button(
            frame,
            relief='flat',
            highlightthickness=0,
            bg=Color.accent,
            fg=Color.button_text,
            activebackground=Color.hover,
            activeforeground=Color.button_text
        )
        button.configure(text=text, font=Font.button, command=command)
        button.pack_configure(padx=25, pady=18, ipadx=70, ipady=8, fill='x')


def _go_to_scene(scene: Callable[[Tk], None], tk: Tk, frame: Frame) -> Callable[[], None]:
    def go_to():
        scene(tk)
        frame.destroy()
    return go_to


def make_help(tk: Tk):
    frame = Frame(tk, bg=Color.background, padx=10, pady=30)
    frame.place_configure(relx=0.5, rely=0.5, anchor='center')
    label = Label(
        frame,
        relief='flat',
        highlightthickness=0,
        bg=Color.background,
        fg=Color.label_text,
        text='ping-pong',
        font=Font.header
    )
    label.pack_configure(padx=30, pady=5, ipadx=30, ipady=5)
    label = Label(
        frame,
        relief='flat',
        highlightthickness=0,
        bg=Color.background,
        fg=Color.label_text,
        text=(
            'It\'s a classic ping-pong game, where you\'re to hit the ball\n'
            'using the paddle. The more ball doesn\'t hit the floor, the\n'
            'more points you score. Use left and right arrows to move the\n'
            'paddle. Hit special targets to score extra points.'
        ),
        font=Font.description
    )
    label.pack_configure(padx=30, pady=5, ipadx=30, ipady=5)
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
    button.pack_configure(padx=25, pady=15, ipadx=130, ipady=10)

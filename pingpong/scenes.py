from tkinter import Tk, Frame, Button
from typing import Callable
from pingpong.theme import Color, Font


def make_main_menu(tk: Tk):
    frame = Frame(
        tk,
        highlightthickness=2,
        bg=Color.background,
        highlightbackground=Color.accent,
        padx=5,
        pady=10
    )
    frame.place_configure(relx=0.5, rely=0.5, anchor='center')
    options = [('Help', _go_to_scene(make_help_menu, tk, frame)), ('Quit', tk.quit)]
    for text, command in options:
        button = Button(
            frame,
            relief='flat',
            highlightthickness=0,
            bg=Color.accent,
            fg=Color.text,
            activebackground=Color.hover,
            activeforeground=Color.text
        )
        button.configure(text=text, font=Font.button, command=command)
        button.pack_configure(padx=25, pady=18, ipadx=70, ipady=8, fill='x')


def _go_to_scene(scene: Callable[[Tk], None], tk: Tk, frame: Frame) -> Callable[[], None]:
    def go_to():
        scene(tk)
        frame.destroy()
    return go_to


def make_help_menu(tk: Tk):
    frame = Frame(tk, bg=Color.background, padx=10, pady=30)
    frame.place_configure(relx=0.5, rely=0.5, anchor='center')

    button = Button(
        frame,
        relief='flat',
        highlightthickness=0,
        bg=Color.accent,
        fg=Color.text,
        activebackground=Color.hover,
        activeforeground=Color.text
    )
    button.configure(
        text='Back',
        font=Font.button,
        command=_go_to_scene(make_main_menu, tk, frame)
    )
    button.pack_configure(padx=25, pady=15, ipadx=130, ipady=10)

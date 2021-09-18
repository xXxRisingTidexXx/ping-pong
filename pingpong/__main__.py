from tkinter import Tk


def main():
    tk = Tk()
    tk.wm_title('ping-pong')
    tk.wm_geometry(f'{tk.winfo_screenwidth()}x{tk.winfo_screenheight()}')
    tk.wm_resizable(0, 0)
    tk.wm_attributes('-topmost', 1, '-type', 'splash')
    tk.configure(background='#000000')

    try:
        tk.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
from tkinter import *
from PIL import Image, ImageTk

# create root window
root = Tk()


class Window(Frame):

    # creating main window/frame)
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    # creation of init window
    def init_window(self):
        # set title of the window to "GUI"
        self.master.title("GUI")
        # allow widget to take full space of the root window
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label="Save")
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu, tearoff=0)
        edit.add_command(label="Undo")
        edit.add_command(label="Redo")
        menu.add_cascade(label="Edit", menu=edit)

        themes = Menu(menu, tearoff=0)
        themes.add_command(label="White")
        themes.add_command(label="Grey")
        themes.add_command(label="Black")
        menu.add_cascade(label="Themes", menu=themes)

        toolbar = Menu(self)

        toolbar_menu = Menu(toolbar)
        toolbar.add_cascade(label="Test", menu=toolbar_menu)

        txt = Text(self, height=150, width=200)
        txt.pack(side=TOP, fill=BOTH)
        txt.focus()

    def client_exit(self):
        exit()


# set window size
root.geometry("1280x720")

# create instance of root window
app = Window(root)
# begin main loop
root.mainloop()

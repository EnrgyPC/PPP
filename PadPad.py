from tkinter import *

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
        self.master.config(menu = menu)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)


    def show_img(self):
        load = Image.open()

    def client_exit(self):
        exit()


# set window size
root.geometry("480x320")

# create instance of root window
app = Window(root)
# begin main loop
root.mainloop()

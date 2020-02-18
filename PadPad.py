import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk


class PadPad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.FONT_SIZE = 12
        self.FONT = "Liberation Sans"
        self.WINDOW_TITLE = "PPP - PyPadPad"

        self.BG_COLOR = "lightgrey"
        self.FG_COLOR = "black"

        self.F_TYPES = (("Text file", "*.txt"), ("All files", "*.*"))

        self.THEMES = [
            "White",
            "Grey",
            "Black"
        ]

        self.IMAGES = {
            "new_file": "new.png"
        }

        # doesn't work
        self.geometry = "1024x768"

        self.open_file = ""
        self.title(self.WINDOW_TITLE + self.open_file)

        # bindings

        self.bind("<Button-3>", self.show_context_menu)

        # popup menu

        self.context_menu = tk.Menu(self, tearoff=0, bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.context_menu.add_command(label="Copy")
        self.context_menu.add_command(label="Cut")
        self.context_menu.add_command(label="Paste")
        self.context_menu.bind("<Leave>", self.close_context_menu)

        # menus

        self.menu = tk.Menu(self, bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.config(menu=self.menu)

        self.file = tk.Menu(self.menu, tearoff=0, bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.file.add_command(label="New", command=self.create_new_dialog, accelerator="Ctrl+N")
        self.file.add_command(label="Open...", command=self.open_file_dialog, accelerator="Ctrl+O")
        self.file.add_command(label="Save", command=self.save_file_dialog, accelerator="Ctrl+S")
        self.file.add_separator()
        self.file.add_command(label="Exit", command=client_exit)
        self.menu.add_cascade(label="File", menu=self.file)

        self.edit = tk.Menu(self.menu, tearoff=0, bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.edit.add_command(label="Undo")
        self.edit.add_command(label="Redo")
        self.menu.add_cascade(label="Edit", menu=self.edit)

        self.settings = tk.Menu(self.menu, tearoff=0, bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.settings.add_command(label="Themes")
        self.settings.add_command(label="Preferences")
        self.menu.add_cascade(label="Settings", menu=self.settings)

        # toolbar

        self.toolbar = tk.Frame(self, bd=1, relief="raised", bg=self.BG_COLOR)
        self.new_file_img = Image.open(self.IMAGES.get("new_file"))
        self.nf_img = ImageTk.PhotoImage(self.new_file_img, size=16)
        self.new_file_button = tk.Button(self.toolbar, image=self.nf_img, relief="flat", bg=self.BG_COLOR,
                                         command=self.create_new_dialog)
        self.new_file_button.pack(side="left", padx=2, pady=2)
        self.toolbar.pack(side="top", fill="x")

        # textbox

        self.txt = scrolledtext.ScrolledText(self, font=(self.FONT, self.FONT_SIZE), padx=5, pady=5)
        self.txt.pack(fill="both", expand=1)
        self.txt.focus()

    def create_new_dialog(self, event=None):
        save_work_box = tk.messagebox.askyesno("New File", "Save current work before creating new file?")
        if save_work_box:
            file_save = filedialog.asksaveasfile(title="Save file to...", filetypes=self.F_TYPES,
                                                 defaultextension=".txt")
            if file_save is None:
                return
            text_to_save = str(self.txt.get(1.0, tk.END))
            file_save.write(text_to_save)
            file_save.close()
            self.txt.delete(1.0, tk.END)
            self.title(" - ".join([self.WINDOW_TITLE, "Untitled"]))
        else:
            self.txt.delete(1.0, tk.END)
            self.title(" - ".join([self.WINDOW_TITLE, "Untitled"]))

    def open_file_dialog(self, event=None):
        file_to_open = filedialog.askopenfilename(title="Open file from...", filetypes=self.F_TYPES,
                                                  defaultextension=".txt", initialdir="/")
        if file_to_open:
            self.open_file = file_to_open
            self.txt.delete(1.0, tk.END)

            with open(file_to_open, "r") as file_contents:
                file_lines = file_contents.readlines()
                if len(file_lines) > 0:
                    for index, line in enumerate(file_lines):
                        index = float(index) + 1.0
                        self.txt.insert(index, line)

            self.title(" - ".join([self.WINDOW_TITLE, self.open_file]))

    def save_file_dialog(self, event=None):
        if not self.open_file:
            file_to_save = filedialog.asksaveasfilename(title="Save file to...", filetypes=self.F_TYPES,
                                                        defaultextension=".txt", initialdir="/")
            if file_to_save:
                self.open_file = file_to_save

        if self.open_file:
            new_contents = self.txt.get(1.0, tk.END)
            with open(self.open_file, "w") as open_file:
                open_file.write(new_contents)

    def show_context_menu(self, pos):
        self.context_menu.post(pos.x_root, pos.y_root)

    def close_context_menu(self, pos):
        self.context_menu.unpost()


def client_exit():
    exit()


if __name__ == '__main__':
    text_editor = PadPad()
    text_editor.mainloop()

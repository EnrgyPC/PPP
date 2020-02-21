import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser


class PadPad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.FONT_SIZE = 12
        self.FONT = "Liberation Sans"
        self.WINDOW_TITLE = "PPP - PyPadPad"
        self.VERSION_NUMBER = "0.1.2"

        self.BG_COLOR = "lightgrey"
        self.FG_COLOR = "black"

        self.F_TYPES = (("Text file", "*.txt"), ("All files", "*.*"))

        self.THEMES = [
            "White",
            "Grey",
            "Black"
        ]

        self.IMAGES = {
            "new_file": "new.png",
            "open_file": "open.png",
            "save_file": "save.png"
        }

        self.open_file = ""
        self.title(self.WINDOW_TITLE + " - " + self.VERSION_NUMBER + self.open_file)

        # bindings

        self.bind("<Button-3>", self.show_context_menu)
        self.bind("<Control-s>", self.save_file_dialog)
        self.bind("<Control-o>", self.open_file_dialog)
        self.bind("<Control-n>", self.create_new_dialog)
        self.bind("<Control-S>", self.save_file_dialog)
        self.bind("<Control-O>", self.open_file_dialog)
        self.bind("<Control-N>", self.create_new_dialog)

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
        self.edit.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.edit.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        self.menu.add_cascade(label="Edit", menu=self.edit)

        self.settings = tk.Menu(self.menu, tearoff=0, bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.settings.add_command(label="Themes")
        self.settings.add_command(label="Preferences")
        self.menu.add_cascade(label="Settings", menu=self.settings)

        self.help = tk.Menu(self.menu, tearoff=0, bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.help.add_command(label="Shortcuts", command=lambda: self.show_shortcut_window())
        self.menu.add_cascade(label="Help", menu=self.help)

        self.about = tk.Menu(self.menu, tearoff=0, bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.about.add_command(label="Version: " + self.VERSION_NUMBER, command=visit_repo)
        self.menu.add_cascade(label="About", menu=self.about)

        # toolbar

        self.toolbar = tk.Frame(self, bd=1, relief="raised", bg=self.BG_COLOR)

        self.new_file_img = Image.open(self.IMAGES.get("new_file"))
        self.nf_img = ImageTk.PhotoImage(self.new_file_img)
        self.new_file_button = tk.Button(self.toolbar, image=self.nf_img, relief="flat", bg=self.BG_COLOR,
                                         command=self.create_new_dialog)
        self.new_file_button.pack(side="left", padx=2, pady=2)

        self.open_file_img = Image.open(self.IMAGES.get("open_file"))
        self.of_img = ImageTk.PhotoImage(self.open_file_img)
        self.open_file_button = tk.Button(self.toolbar, image=self.of_img, relief="flat", bg=self.BG_COLOR,
                                          command=self.open_file_dialog)
        self.open_file_button.pack(side="left", padx=2, pady=2)

        self.save_file_img = Image.open(self.IMAGES.get("save_file"))
        self.sf_img = ImageTk.PhotoImage(self.save_file_img)
        self.save_file_button = tk.Button(self.toolbar, image=self.sf_img, relief="flat", bg=self.BG_COLOR,
                                          command=self.save_file_dialog)
        self.save_file_button.pack(side="left", padx=2, pady=2)

        self.toolbar.pack(side="top", fill="x")

        # textbox

        self.txt = scrolledtext.ScrolledText(self, font=(self.FONT, self.FONT_SIZE), padx=5, pady=5)
        self.txt.config(undo=1, autoseparators=1, maxundo=-1)
        self.txt.pack(fill="both", expand=1)
        self.txt.focus()

        # textbox bindings

        self.txt.bind("<Tab>", self.make_space)
        self.txt.bind("<Control-a>", self.select_all)
        self.txt.bind("<Control-z>", self.undo)
        self.txt.bind("<Control-y>", self.redo)
        self.txt.bind("<Control-A>", self.select_all)
        self.txt.bind("<Control-Z>", self.undo)
        self.txt.bind("<Control-Y>", self.redo)

    def show_shortcut_window(self, event=None):

        # shortcut window

        shortcut_window = tk.Toplevel(self, bg=self.BG_COLOR)
        shortcut_window.title("Shortcuts")
        shortcut_window.geometry("250x350")
        shortcut_window.resizable(False, False)

        # shortcuts

        general_bindings = {
            "Right Click": "Show Context Menu",
            "Control + S": "Save File",
            "Control + O": "Open File",
            "Control + N": "New File",
        }

        textbox_bindings = {
            "Tab": "Make Space",
            "Control + A": "Select All",
            "Control + Z": "Undo",
            "Control + Y": "Redo",
        }

        general_shortcut_frame = tk.LabelFrame(shortcut_window, text="General", padx=5, pady=5)
        general_shortcut_frame.pack(fill="x", expand=1)

        general_shortcut_box = tk.Listbox(general_shortcut_frame, bg=self.BG_COLOR,
                                          bd=2, height=7)
        for binding, desc in zip(general_bindings.keys(), general_bindings.values()):
            general_shortcut_box.insert(tk.END, binding + " - " + desc)

        general_shortcut_box.pack(fill="x", expand=1)

        textbox_shortcut_frame = tk.LabelFrame(shortcut_window, text="Text Editor", padx=5, pady=5)
        textbox_shortcut_frame.pack(fill="x", expand=1)

        textbox_shortcut_box = tk.Listbox(textbox_shortcut_frame, bg=self.BG_COLOR,
                                          bd=2, height=7)
        for binding, desc in zip(textbox_bindings.keys(), textbox_bindings.values()):
            textbox_shortcut_box.insert(tk.END, binding + " - " + desc)

        textbox_shortcut_box.pack(fill="x", expand=1)

    def undo(self, event=None):
        self.txt.edit_undo()
        return "break"

    def redo(self, event=None):
        self.txt.edit_redo()
        return "break"

    def make_space(self, event=None):
        self.txt.insert(tk.INSERT, "    ")
        return "break"

    def select_all(self, event):
        self.txt.tag_add(tk.SEL, "1.0", tk.END)
        self.txt.mark_set(tk.INSERT, "1.0")
        self.txt.see(tk.INSERT)
        return "break"

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
            self.title(" - ".join([self.WINDOW_TITLE, self.VERSION_NUMBER, "Untitled"]))
        else:
            self.txt.delete(1.0, tk.END)
            self.title(" - ".join([self.WINDOW_TITLE, self.VERSION_NUMBER, "Untitled"]))

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


def visit_repo():
    webbrowser.open("https://github.com/EnrgyPC/PPP", new=1, autoraise=True)


def client_exit():
    exit()


if __name__ == '__main__':
    text_editor = PadPad()
    text_editor.geometry("1280x720")
    text_editor.mainloop()

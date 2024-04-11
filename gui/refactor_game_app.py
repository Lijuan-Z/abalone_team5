import _tkinter
import tkinter as tk
from tkinter import ttk, font

from gui.refactor_game.config_page import ConfigPage
from gui.refactor_game.game_page import GamePage

dark_mode_colors = {
    'Background': ("#2D2D2D", "#FFFFFF"),
    'Label': ("#2D2D2D", "#FFFFFF"),
    'Button': ("#4E4E4E", "#FFFFFF"),
    'Entry': ("#2D2D2D", "#FFFFFF"),
    'Text': ("#2D2D2D", "#FFFFFF"),
    'Frame': ("#2D2D2D", "#FFFFFF"),
    'Select': ("#555555", "#FFFFFF"),
    'Scrollbar': ("#4E4E4E", "#2D2D2D"),
    'Canvas': ("#4E4E4E", "#2D2D2D")

    # 'GameDisplayState': ("#FFFFFF", "#FFFFFF"),
    # 'GamePage': ("#FFFFFF", "#FFFFFF"),
}


class GameApp(tk.Tk):
    """GameApp runs the tkinter app and controls switching between GUIs."""

    def __init__(self, backend_conn, *args, **kwargs):
        """Initializes a new GameApp instance.

        :param args: any args to pass through to tk.Tk
        :param kwargs: any kwargs to pass through to tk.Tk
        """
        super().__init__()

        self.backend_conn = backend_conn

        self.title("Abalone")
        self.resizable = True
        # self.defaultFont = font.Font(family="Times New Roman", size=50)
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=12)

        self.default_font = font.nametofont("TkTextFont")
        self.default_font.configure(size=12)

        self.default_font = font.nametofont("TkFixedFont")
        self.default_font.configure(size=14)
        # self.attributes('-fullscreen', True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_page = None
        self.app_theme = None

        self.combobox_theme_init()
        self.dark_mode(root=self)

        self.start_config()
        # self.start_game(config=None)

    def start_config(self, **kwargs):
        """Starts the config page."""
        if self.current_page:
            self.forget_packs_recursively(self)
        self.geometry("800x800")
        self.center(self)
        self.current_page = ConfigPage(self, next_page_callback=self.start_game, **kwargs)
        self.current_page.grid(row=0, column=0, sticky='nesw')
        self.dark_mode(root=self)

    def start_game(self, **kwargs):
        """Starts the game page."""
        if self.current_page:
            self.forget_packs_recursively(self)
        self.geometry("1200x800")
        self.center(self)
        self.current_page = GamePage(self, back_to_config_callback=self.start_config, backend_conn=self.backend_conn, **kwargs)
        self.current_page.grid(row=0, column=0, sticky='nsew')
        self.dark_mode(root=self)


    def center(self, win):
        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y//5))
        win.deiconify()

    def forget_packs_recursively(self, parent):
        """Recursively forgets all child widgets of the given parent widget.

        :param parent: Tkinter widget that acts as the parent of other widgets.
        """
        for child in parent.winfo_children():
            child.pack_forget()
            self.forget_packs_recursively(child)

    def combobox_theme_init(self):
        """Initializes the available themes for combobox widgets."""
        self.app_theme = ttk.Style()
        self.app_theme.theme_create('combobox_theme_dark',
                                    parent='alt',
                                    settings={
                                        'TCombobox': {
                                            'configure': {
                                                'selectbackground': '#353535',
                                                'fieldbackground': '#656565',
                                                'foreground': '#FFFFFF'
                                            }
                                        }
                                    }
                                    )

        self.app_theme.theme_create('combobox_theme_light', parent='alt',
                                    settings={
                                        'TCombobox': {
                                            'configure': {
                                                'selectbackground': 'blue',
                                                'fieldbackground': 'purple',
                                                'background': 'pink'
                                            }
                                        }
                                    }
                                    )

    def dark_mode(self, root):
        """Re-colors root to be dark mode, then recurses."""
        self.configure(bg=dark_mode_colors['Background'][0])
        self.dark_mode_recurse(root=root)
        self.app_theme.theme_use('combobox_theme_dark')

    def light_mode(self, root):
        """Re-colors root to be light mode."""
        self.app_theme.theme_use('combobox_theme_light')

    def dark_mode_recurse(self, root):
        """Recursively darken root's children to be dark mode."""
        for widget in root.winfo_children():
            self.dark_mode(widget)
            widget_type = widget.winfo_class()
            parent_class = widget.__class__.__name__
            # print(f"dark moding: {parent_class} of type: {widget_type}")
            if widget.__class__.__name__ in dark_mode_colors.keys():
                try:
                    widget.configure(
                        background=dark_mode_colors[parent_class][0])
                except _tkinter.TclError as e:
                    # print(e)
                    pass
                try:
                    widget.configure(
                        foreground=dark_mode_colors[parent_class][1])
                except _tkinter.TclError as e:
                    # print(e)
                    pass

                try:
                    widget.configure(
                        selectbackground=dark_mode_colors[parent_class][2])
                except (_tkinter.TclError, IndexError) as e:
                    # print(e)
                    pass

                try:
                    widget.configure(
                        fieldbackground=dark_mode_colors[parent_class][3])
                except (_tkinter.TclError, IndexError) as e:
                    # print(e)
                    pass
            elif widget_type in dark_mode_colors.keys():
                try:
                    widget.configure(
                        background=dark_mode_colors[widget_type][0])
                except _tkinter.TclError as e:
                    # print(e)
                    pass
                try:
                    widget.configure(
                        foreground=dark_mode_colors[widget_type][1])
                except _tkinter.TclError as e:
                    # print(e)
                    pass

                try:
                    widget.configure(
                        selectbackground=dark_mode_colors[widget_type][2])
                except (_tkinter.TclError, IndexError) as e:
                    # print(e)
                    pass

                try:
                    widget.configure(
                        fieldbackground=dark_mode_colors[widget_type][3])
                except (_tkinter.TclError, IndexError) as e:
                    # print(e)
                    pass
            else:
                if widget_type not in ['TCombobox']:
                    print(f"{widget_type} not recognized for coloring")

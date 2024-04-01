import _tkinter
import tkinter as tk
from tkinter import ttk

from gui.refactor_game.config_page import ConfigPage
from gui.refactor_game.game_page import GamePage

dark_mode_colors = {
    'Background': ("#2D2D2D", "#CCCCCC"),
    'Label': ("#2D2D2D", "#CCCCCC"),
    'Button': ("#4E4E4E", "#CCCCCC"),
    'Entry': ("#333333", "#CCCCCC"),
    'Text': ("#333333", "#CCCCCC"),
    'Frame': ("#2D2D2D", "#CCCCCC"),
    'Select': ("#555555", "#CCCCCC"),
    'Scrollbar': ("#4E4E4E", "#2D2D2D"),
}


class GameApp(tk.Tk):
    """GameApp runs the tkinter app and controls switching between GUIs."""

    def __init__(self, *args, **kwargs):
        """Initializes a new GameApp instance.

        :param args: any args to pass through to tk.Tk
        :param kwargs: any kwargs to pass through to tk.Tk
        """

        super().__init__()
        self.title("Abalone")
        self.resizable = True
        # self.attributes('-fullscreen', True)

        self.current_page = None
        self.app_theme = None
        self.combobox_theme_init()
        # self.dark_mode(root=self)

        self.start_config(next_page_callback=self.start_game)

    def start_config(self, **kwargs):
        """Starts the config page."""
        if self.current_page:
            self.forget_packs_recursively(self)
        self.geometry("800x800")
        self.current_page = ConfigPage(self,
                                       **kwargs)
        self.current_page.pack(anchor=tk.E, expand=True, fill=tk.BOTH)
        self.dark_mode(root=self)

    def start_game(self, **kwargs):
        """Starts the game page."""
        if self.current_page:
            self.forget_packs_recursively(self)
        self.geometry("400x400")
        self.current_page = GamePage(self, **kwargs)
        self.current_page.pack(anchor=tk.CENTER, expand=True)
        self.dark_mode(root=self)

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
                                                'foreground': '#CCCCCC'
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
            print(f"dark moding {widget_type}")
            if widget_type in dark_mode_colors.keys():
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
                    print(e)
                    pass

                try:
                    widget.configure(
                        fieldbackground=dark_mode_colors[widget_type][3])
                except (_tkinter.TclError, IndexError) as e:
                    print(e)
                    pass
            else:
                print(f"{widget_type} not recognized for coloring")

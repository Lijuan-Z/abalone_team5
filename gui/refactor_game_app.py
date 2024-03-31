import _tkinter
import tkinter as tk

from gui.refactor_game.config_page import ConfigPage
from gui.refactor_game.game_page import GamePage

dark_mode_colors = {
    'Background': ("#2D2D2D", "#CCCCCC"),
    'Label': ("#333333", "#CCCCCC"),
    'Button': ("#4E4E4E", "#CCCCCC"),
    'Entry': ("#333333", "#CCCCCC"),
    'Text': ("#333333", "#CCCCCC"),
    'Frame': ("#2D2D2D", "#CCCCCC"),
    'Select': ("#555555", "#CCCCCC"),
    'Scrollbar': ("#4E4E4E", "#2D2D2D"),
    'TCombobox': ("#000000", "#000000")
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
        # self.resizable = True
        # self.attributes('-fullscreen', True)

        self.current_page = None

        self.start_config(next_page_callback=self.start_game)

    def start_config(self, **kwargs):
        if self.current_page:
            self.forget_packs_recursively(self)
        self.geometry("400x300")
        self.current_page = ConfigPage(self,
                                       **kwargs)
        self.current_page.pack()
        self.dark_mode(root=self)

    def start_game(self, **kwargs):
        # Hide the config screen and show the game screen
        if self.current_page:
            self.forget_packs_recursively(self)
        self.geometry("400x400")
        self.current_page = GamePage(self, **kwargs)
        self.current_page.pack()
        self.dark_mode(root=self)

    def forget_packs_recursively(self, parent):
        """
        Recursively forgets all child widgets of the given parent widget.

        :param parent: A Tkinter widget that acts as the parent of other widgets.
        """
        for child in parent.winfo_children():
            child.pack_forget()
            self.forget_packs_recursively(child)  # Recursively forget children's children

    def dark_mode(self, root):
        """Re-colors root to be dark mode, then recurses."""
        self.configure(bg=dark_mode_colors['Background'][0])
        self.dark_mode_recurse(root=root)

    def dark_mode_recurse(self, root):
        """Recursively darken root's children to be dark mode."""
        for widget in root.winfo_children():
            self.dark_mode(widget)
            widget_type = widget.winfo_class()
            # print(f"dark moding {widget_type}")
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
            else:
                print(f"{widget_type} not recognized for coloring")

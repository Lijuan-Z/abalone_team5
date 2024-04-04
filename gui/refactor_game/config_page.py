import tkinter as tk
from tkinter import ttk
from pprint import pprint
from enum import Enum


class ExtendedEnum(Enum):
    """Like a regular enum but with the ability to list."""

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Layout(ExtendedEnum):
    """Board layout options."""
    STANDARD = "Standard"
    BELGIAN_DAISY = "Belgian daisy"
    GERMAN_DAISY = "German daisy"


class Operator(ExtendedEnum):
    """Operator type options."""
    HUMAN = "Human"
    AI = "AI"


class Color(ExtendedEnum):
    """Marble color options."""
    BLACK = "Black"
    WHITE = "White"


class MiscOptions(ExtendedEnum):
    """Miscellaneous options."""
    UNLIMITED_STRING = "Unlimited"
    UNLIMITED_QUANTITY = float('inf')


class ConfigDisplayState(tk.Frame):
    """Stores and displays the display state of the config page.

    Display state is state of the 'frontend'
    """

    ASCII_TITLE = """
         _           _                  
   /\\   | |         | |                 
  /  \\  | |__   __ _| | ___  _ __   ___ 
 / /\\ \\ | '_ \\ / _` | |/ _ \\| '_ \\ / _ \\
/ ____ \\| |_) | (_| | | (_) | | | |  __/
/_/    \\_\\_.__/ \\__,_|_|\\___/|_| |_|\\___| 
 
    """

    TURN_OPTIONS = [
        "10",
        "30",
        "40",
        MiscOptions.UNLIMITED_STRING.value,
    ]

    TIME_OPTIONS = [
        "1",
        "5",
        "10",
        "30",
        "90",
        MiscOptions.UNLIMITED_STRING.value,
    ]

    def __init__(self, parent, next_page_callback, **kwargs):
        super().__init__(parent)

        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure(0, weight=1)

        self.parent = parent
        self.start_game_callback = next_page_callback

        # dictionary of components
        self.comps = {}

        # dictionary of variables
        self.vars = {}

        frame = tk.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)


        frame.rowconfigure(0, weight=4) # blank space on top
        frame.rowconfigure(1, weight=4) # title
        frame.rowconfigure(2, weight=1) # layout options
        frame.rowconfigure(3, weight=1) # blank space
        frame.rowconfigure((4,5,6,7,8,9,10,11), weight=1), # options/labels
        frame.rowconfigure(12, weight=1) # start button
        frame.rowconfigure(13, weight=20) # blank space on bottom

        self._pack_title(parent=frame)
        self._pack_choices(parent=frame)
        self._pack_start_button(parent=frame, start_game_callback=self.start_game_callback)

        frame.grid(row=0, column=1, sticky='nsew')

    def _get_config(self):
        config ={
            'layout': self.comps['layout_combobox'].get(),

            'player_1_color': self.comps['player_1_color_combobox'].get(),
            'player_1_operator': self.comps['player_1_operator_combobox'].get(),
            'player_1_seconds_per_turn': _int_or_none(
                self.comps['player_1_seconds_per_turn_combobox'].get()
            ),
            'player_1_turn_limit': _int_or_none(
                self.comps['player_1_turn_limit_combobox'].get()
            ),
            'player_2_color': self.comps['player_2_color_combobox'].get(),
            'player_2_operator': self.comps[
                'player_2_operator_combobox'].get(),
            'player_2_seconds_per_turn': _int_or_none(
                self.comps['player_2_seconds_per_turn_combobox'].get()
            ),
            'player_2_turn_limit': _int_or_none(
                self.comps['player_2_turn_limit_combobox'].get()
            ),
        }
        return config

    def _set_config(self, config):
        """TODO: have this set the current config to the incoming one."""

    def _pack_start_button(self, parent, start_game_callback):
        """Packs the start button."""
        start_game_button = tk.Button(parent,
                                      text="Start Game",
                                      command=
                                      lambda: start_game_callback(
                                          config=self._get_config()
                                      )
                                      )

        start_game_button.grid(row=12, column=0, columnspan=2, pady=20)

    def _pack_title(self, parent):
        """Packs the title."""
        title_string = tk.StringVar()
        title_string.set(ConfigDisplayState.ASCII_TITLE)

        title_label = tk.Label(parent,
                               textvariable=title_string,
                               font=('Courier', 20, 'bold'))

        self.comps['title_label'] = title_label
        self.comps['title_label'].grid(row=1,
                                       column=0,
                                       columnspan=2,
                                       pady=(0, 5),
                                       sticky='new')

    def _pack_choices(self, parent):
        """Packs the choices."""

        pady = (5, 0)

        self._pack_selection_combobox(parent,
                                      "layout",
                                      Layout.list(),
                                      dict(row=2, column=0, columnspan=2, padx=50, pady=pady, sticky='n'))

        self._pack_selection_combobox(parent,
                                      "player_1_operator",
                                      Operator.list(),
                                      dict(row=4, column=0, pady=pady, sticky='n'))

        self._pack_selection_combobox(parent,
                                      "player_1_color",
                                      Color.list(),
                                      dict(row=6, column=0, pady=pady, sticky='n'))

        self._pack_selection_combobox(parent,
                                      "player_1_turn_limit",
                                      self.TURN_OPTIONS,
                                      dict(row=8, column=0, pady=pady, sticky='n'),
                                      readonly=False,
                                      default_index=2)

        self._pack_selection_combobox(parent,
                                      "player_1_seconds_per_turn",
                                      self.TIME_OPTIONS,
                                      dict(row=10, column=0, padx=pady, sticky='n'),
                                      readonly=False,
                                      default_index=4)

        self._pack_selection_combobox(parent,
                                      "player_2_operator",
                                      Operator.list(),
                                      dict(row=4, column=1, pady=pady, sticky='n'),
                                      1)

        self._pack_selection_combobox(parent,
                                      "player_2_color",
                                      Color.list(),
                                      dict(row=6, column=1, pady=pady, sticky='n'),
                                      1)

        self._pack_selection_combobox(parent,
                                      "player_2_turn_limit",
                                      self.TURN_OPTIONS,
                                      dict(row=8, column=1, pady=pady, sticky='n'),
                                      readonly=False,
                                      default_index=2)

        self._pack_selection_combobox(parent,
                                      "player_2_seconds_per_turn",
                                      self.TIME_OPTIONS,
                                      dict(row=10, column=1, pady=pady, sticky='n'),
                                      readonly=False,
                                      default_index=2)

    def _pack_selection_combobox(self, parent, option_string, options_list,
                                 grid_config, default_index=0, readonly=True):
        """Packs the layout selection dropdown."""
        formatted_option_string = option_string
        formatted_option_string = formatted_option_string.split("_")
        formatted_option_string = " ".join(formatted_option_string)
        formatted_option_string = formatted_option_string.title()

        layout_selection_label = tk.Label(parent,
                                          text=f"{formatted_option_string}:")
        layout_selection_label.grid(**grid_config)

        layout_selection_combobox = (
            ttk.Combobox(parent,
                         values=options_list,
                         state='readonly' if readonly else '',
                         background="#000000")
        )
        layout_selection_combobox.current(default_index)

        self.comps[f'{option_string}_combobox'] = layout_selection_combobox

        grid_config['row'] += 1
        self.comps[f'{option_string}_combobox'].grid(**grid_config)

    def _pack_selection_entry(self, parent, option_string,
                              entry_init_string, grid_config):
        """Packs the layout selection dropdown."""
        formatted_option_string = option_string
        formatted_option_string = formatted_option_string.split("_")
        formatted_option_string = " ".join(formatted_option_string)
        formatted_option_string = formatted_option_string.title()

        layout_selection_label = tk.Label(parent,
                                          text=f"{formatted_option_string}:")
        layout_selection_label.grid(**grid_config)

        layout_selection_entry = ttk.Entry(parent)
        layout_selection_entry.insert(0, entry_init_string)

        self.comps[f'{option_string}_entry'] = layout_selection_entry

        grid_config['row'] += 1
        self.comps[f'{option_string}_entry'].grid(**grid_config)


class ConfigPage(tk.Frame):
    """Allows user to enter configs before they begin the game."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.display_state = ConfigDisplayState(parent=parent, **kwargs)
        self.display_state.grid(row=0, column=0, sticky='nesw')

    def color_overrides(self):
        """place to put overriding colors"""
        pass


def _int_or_none(string: str):
    """Attempts to cast to string, else returns None."""
    if string == MiscOptions.UNLIMITED_STRING.value:
        return MiscOptions.UNLIMITED_QUANTITY.value
    else:
        return int(string)

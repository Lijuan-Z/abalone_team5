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
    UNLIMITED = "Unlimited"


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
    ]

    TIME_OPTIONS = [
        "1",
        "5",
        "10",
        "30",
        "90",
    ]

    def __init__(self, parent, next_page_callback, **kwargs):
        super().__init__(parent)

        self.parent = parent
        self.start_game_callback = next_page_callback

        # dictionary of components
        self.comps = {}

        # dictionary of variables
        self.vars = {}

        self._pack_title()
        self._pack_choices()
        self._pack_start_button(start_game_callback=self.start_game_callback)

        pprint(self.comps)

    def _pack_start_button(self, start_game_callback):
        """Packs the start button."""

        config = config = {
            'layout': self.comps['layout_combobox'].get(),
            'player_1_color': self.comps['player_1_color_combobox'].get(),
            'player_1_operator': self.comps[
                'player_1_operator_combobox'].get(),
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

        start_game_button = tk.Button(self,
                                      text="Start Game",
                                      command=
                                      lambda: start_game_callback(
                                          config=config
                                      )
                                      )

        start_game_button.grid(row=99, column=1, pady=20)

    def _pack_title(self):
        """Packs the title."""
        title_string = tk.StringVar()
        title_string.set(ConfigDisplayState.ASCII_TITLE)

        title_label = tk.Label(self,
                               textvariable=title_string,
                               font=('Courier', 15, 'bold'),
                               anchor=tk.CENTER,
                               justify=tk.LEFT)

        self.comps['title_label'] = title_label
        self.comps['title_label'].grid(row=0,
                                       column=0,
                                       columnspan=99,
                                       pady=(0, 5))

    def _pack_choices(self):
        """Packs the choices."""
        self._pack_selection_combobox("layout",
                                      Layout.list(),
                                      dict(row=1, column=1, pady=(5, 0)))

        self._pack_selection_combobox("player_1_operator",
                                      Operator.list(),
                                      dict(row=3, column=0, pady=(5, 0)))

        self._pack_selection_combobox("player_1_color",
                                      Color.list(),
                                      dict(row=5, column=0, pady=(5, 0)))

        self._pack_selection_combobox("player_1_turn_limit",
                                      self.TURN_OPTIONS
                                      + [MiscOptions.UNLIMITED.value],
                                      dict(row=7, column=0, pady=(5, 0)),
                                      readonly=False,
                                      default_index=2)

        self._pack_selection_combobox("player_1_seconds_per_turn",
                                      self.TIME_OPTIONS
                                      + [MiscOptions.UNLIMITED.value],
                                      dict(row=9, column=0, padx=(5, 0)),
                                      readonly=False,
                                      default_index=5)

        self._pack_selection_combobox("player_2_operator",
                                      Operator.list(),
                                      dict(row=3, column=2, pady=(5, 0)),
                                      1)

        self._pack_selection_combobox("player_2_color",
                                      Color.list(),
                                      dict(row=5, column=2, pady=(5, 0)),
                                      1)

        self._pack_selection_combobox("player_2_turn_limit",
                                      self.TURN_OPTIONS
                                      + [MiscOptions.UNLIMITED.value],
                                      dict(row=7, column=2, pady=(5, 0)),
                                      readonly=False,
                                      default_index=2)

        self._pack_selection_combobox("player_2_seconds_per_turn",
                                      self.TIME_OPTIONS
                                      + [MiscOptions.UNLIMITED.value],
                                      dict(row=9, column=2, pady=(5, 0)),
                                      readonly=False,
                                      default_index=2)

    def _pack_selection_combobox(self, option_string, options_list,
                                 grid_config, default_index=0, readonly=True):
        """Packs the layout selection dropdown."""
        formatted_option_string = option_string
        formatted_option_string = formatted_option_string.split("_")
        formatted_option_string = " ".join(formatted_option_string)
        formatted_option_string = formatted_option_string.title()

        layout_selection_label = tk.Label(self,
                                          text=f"{formatted_option_string}:")
        layout_selection_label.grid(**grid_config)

        layout_selection_combobox = (
            ttk.Combobox(self,
                         values=options_list,
                         state='readonly' if readonly else '',
                         background="#000000")
        )
        layout_selection_combobox.current(default_index)

        self.comps[f'{option_string}_combobox'] = layout_selection_combobox

        grid_config['row'] += 1
        self.comps[f'{option_string}_combobox'].grid(**grid_config)

    def _pack_selection_entry(self, option_string,
                              entry_init_string, grid_config):
        """Packs the layout selection dropdown."""
        formatted_option_string = option_string
        formatted_option_string = formatted_option_string.split("_")
        formatted_option_string = " ".join(formatted_option_string)
        formatted_option_string = formatted_option_string.title()

        layout_selection_label = tk.Label(self,
                                          text=f"{formatted_option_string}:")
        layout_selection_label.grid(**grid_config)

        layout_selection_entry = ttk.Entry(self)
        layout_selection_entry.insert(0, entry_init_string)

        self.comps[f'{option_string}_entry'] = layout_selection_entry

        grid_config['row'] += 1
        self.comps[f'{option_string}_entry'].grid(**grid_config)


class ConfigPage(tk.Frame):
    """Allows user to enter configs before they begin the game."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        self.display_state = ConfigDisplayState(parent=parent, **kwargs)
        self.display_state.pack(expand=True, anchor=tk.CENTER)


def _int_or_none(string: str):
    """Attempts to cast to string, else returns None."""
    try:
        return int(string)
    except ValueError:
        return None

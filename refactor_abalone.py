"""Runs the REFACTORED abalone program with a GUI."""
from gui.refactor_game_app import GameApp

if __name__ == '__main__':
    game = GameApp()

    #TODO: REMOVE AFTER DEV: simulates clicking the start button right away
    # config = game.current_page.display_state._get_config()
    # game.start_game(config=config)

    game.mainloop()


"""Runs the REFACTORED abalone program with a GUI."""
from multiprocessing import Pipe

from gui.refactor_game_app import GameApp
from backend.ai_daemon import AIDaemon

if __name__ == '__main__':

    parent_conn, child_conn = Pipe()

    backend = AIDaemon(frontend_conn=child_conn)
    backend.start()

    game = GameApp(backend_conn=parent_conn)

    #TODO: REMOVE AFTER DEV: simulates clicking the start button right away
    # config = game.current_page.display_state._get_config()
    # game.start_game(config=config)

    game.mainloop()


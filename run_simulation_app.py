"""Driver program for the simulation app."""

from gui import simulation_app
from simulation.versus_simulation import VersusSimulation

if __name__ == "__main__":
    gui = simulation_app.SimApp()

    sim_driver = VersusSimulation()
    sim_driver.bind_display_callback(gui.display_boardstate)
    sim_driver.start()

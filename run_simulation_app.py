"""Driver program for the simulation app."""

from gui import simulation_app
from simulation.versus_simulation import VersusSimulation

if __name__ == "__main__":

    sim_driver = VersusSimulation()

    app = simulation_app.SimApp(sim_driver)
    app.mainloop()

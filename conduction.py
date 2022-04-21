# HUM-433 Project, Energy Consumption Simulator
# Authors: Daniel Tataru/Erwan Serandour/Romeo Tatti
# Created on 14/04/2022
# Simulation of heat conduction of a building through a wall

import math
import numpy as np
import matplotlib.pyplot as plt
import csv
from heatBalance import HeatBalance


### you have to read the HeatBalance balance object
class ConductionModel():
    """
    compute the heat balance of a building
    """
    def __init__(self):
        self.size = 'default ???'
        self.degree = 'default ???'
        self.isolation = 'default ???'

    def update_window(self, size : int):
        """
        compute new heat balance after update

        :param size: window size
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        ## TODO add correct implemetation
        return HeatBalance()
        

    def update_isolation(self, size : int ):
        """
        compute new heat balance after update
        
        :param size: isolation width
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        ## TODO add correct implemetation
        return HeatBalance()

    def update_orientation(self, degree : int):
        """
        compute new heat balance after update
        
        :param size: building orientation
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        ## TODO add correct implemetation
        return HeatBalance()


# Comuting heat loss through conduction [W] based on inside and outside temperature
def heat_loss_wall(T_out, T_in, A_wall, e_wall, Th_cond_wall):
    U_wall = Th_cond_wall / e_wall
    Q_loss = U_wall * A_wall * (T_out - T_in)
    return Q_loss


# Computing total energy loss [J] from heat loss information
def energy_loss_wall(Q, timestep):
    E_loss = 0
    for i in range(0, len(Q) - 1):
        E_loss = E_loss + (Q[i] + Q[i + 1]) / 2 * timestep
    return E_loss


def update_plot(e_wall):
    # Reading csv temperature data
    T_file = open('geneva_temperature_2weeks.csv')
    T_csvreader = csv.reader(T_file)
    next(T_csvreader)
    T_out = []
    for row in T_csvreader:
        T_out.append(row)
    T_out = np.reshape(np.array(T_out, dtype=np.float32), len(T_out))

    # Constants
    T_in = 20  # K, inside desired temperature (assumed constant)
    A_wall = 40  # m^2, Wall surface area in contact with outside
    timestep = 3600 * 24  # 1-hour timestep between temperature data points
    J2kwh = 2.77778 * 10 ** (-7)  # Conversion coefficient between J and kWh
    Th_cond_wall = 2.25  # W/m/K, concrecte wall themrla Conductivity

    # Running the simulation
    Q_loss = heat_loss_wall(T_out, T_in, A_wall, e_wall)
    E_loss = np.zeros(14)

    for i in range(len(Q_loss) - 1):
        E_loss[i] = (energy_loss_wall(Q_loss[i:i + 2], timestep))
    E_loss = E_loss * J2kwh
    # plt.plot(Q_loss)
    # plt.title('Heat loss (W) as a function of time')
    # plt.show()

    # plt.plot(E_loss)
    # plt.title('Daily energy loss in kWh')
    # plt.show()

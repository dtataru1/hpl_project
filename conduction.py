# HUM-433 Project, Energy Consumption Simulator
# Authors: Daniel Tataru/Erwan Serandour/Romeo Tatti
# Created on 14/04/2022
# Simulation of heat conduction of a building through a wall

import math
import string
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
        self.size = 0.0
        self.degree = 0.0
        self.isolation = 0.1
        self.int_temp = 22.0

    def read_data(self, data_file : string):
        '''
        Getting real-world data from csv file (temperature)
        param data_file: Name of data file to read
        return T_out: vector of outside temperature (hourly)
        '''
        T_file = open(data_file)
        T_csvreader = csv.reader(T_file)
        next(T_csvreader)
        T_out = []
        for row in T_csvreader:
            T_out.append(row)
        T_out = np.reshape(np.array(T_out, dtype=np.float32), len(T_out))
        return T_out



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
        # Constants


        T_out = self.read_data('Temp_Data_basel.csv')
        A_wall = 40 - self.size # m^2, Wall surface area in contact with outside
        J2kwh = 2.77778 * 10 ** (-7)  # Conversion coefficient between J and kWh
        Th_cond_wall = 1.75  # W/m/K, concrecte wall themrla Conductivity
        Th_cond_window = 1.3
        e_window= 0.05
        timestep = 60*60 #1-hour

        Q_loss = Th_cond_wall/self.isolation * A_wall * (T_out - self.int_temp) + Th_cond_window/e_window * self.size *(T_out - self.int_temp)
        E_loss = np.zeros(len(Q_loss)-1)
        for i in range (0, len(Q_loss)-1):
            E_loss[i] = (Q_loss[i]+Q_loss[i+1]) / 2 * timestep

        #E_loss = E_loss*
            

# Computing total energy loss [J] from heat loss information

  

        # for i in range(len(Q_loss) - 1):
        #     E_loss[i] = (energy_loss_wall(Q_loss[i:i + 2], timestep))
        # E_loss = E_loss * J2kwh




        return HeatBalance()

    def update_orientation(self, degree : int):
        """
        compute new heat balance after update
        
        :param size: building orientation
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        ## TODO add correct implemetation

        return HeatBalance()

        

    


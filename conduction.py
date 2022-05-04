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
from heatBalance import HeatBalanceMonth

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

    def read_data(self, data_file):
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
        

    def update_isolation(self, width : int ):
        """
        compute new heat balance after update
        
        :param width: isolation width
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        self.isolation = width

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_temp_idx = [1, 745, 1415, 2161, 2881, 3625, 4345, 5089, 5833, 6553, 7297, 8017, 8760]
        heat_calculations = {}

        T_out = self.read_data('Temp_Data_Basel_2021.csv')
        A_wall = 40 - self.size # m^2, Wall surface area in contact with outside
        J2kwh = 2.77778 * 10 ** (-7)  # Conversion coefficient between J and kWh
        Th_cond_wall = 1.75  # W/m/K, concrecte wall themrla Conductivity
        Th_cond_window = 1.3
        e_window= 0.05
        timestep = 60*60 #1-hour

        for i in range(0, len(months)-1):
            Q_loss = Th_cond_wall/self.isolation * A_wall * (T_out[month_temp_idx[i]:month_temp_idx[i+1]] - self.int_temp) + Th_cond_window/e_window * self.size *(T_out[month_temp_idx[i]:month_temp_idx[i+1]] - self.int_temp)
            E_loss = 0
            for j in range (0, len(Q_loss)-1):
                 E_loss = E_loss+(Q_loss[j]+Q_loss[j+1])/2 * timestep
            E_loss *= J2kwh
            heat_calculations[months[i]] = HeatBalanceMonth(0,0,E_loss)

        return heat_calculations

    def update_orientation(self, degree : int):
        """
        compute new heat balance after update
        
        :param size: building orientation
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        return HeatBalance()

    def compute_heat_balance(self):



        heat_calculations[months[i]] = HeatBalanceMonth(0,0,E_loss)
        return 


test = ConductionModel()

values = test.update_isolation(0.3)
print(values['Jul'].heatLoss)
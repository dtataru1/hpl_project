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
from heatBalance import HeatBalanceWeek

### you have to read the HeatBalance balance object
class ConductionModel():
    """
    compute the heat balance of a building
    """
    def __init__(self):
        self.size = 0.00
        self.degree = 0.0
        self.isolation = 0.05
        self.int_temp = 22.0
        self.T_out, self.I_r, self.sun_angle = self.read_data('Temp_Data_Basel_2021.csv', 'Radiation_Data_Zurich_2018.csv', 'Zenith_Angle_Data_Zurich_2018.csv')
        
    def read_data(self, temp_file, rad_file, angle_file):
        '''
        Getting real-world data from csv file (temperature, solar direct radiation and angle to zenith)
        param data_file: Name of data file to read
        return T_out: vector of outside temperature (hourly)
        '''
        T_file = open(temp_file)
        T_csvreader = csv.reader(T_file)
        next(T_csvreader)
        T_out = []
        for row in T_csvreader:
            T_out.append(row)
        T_out = np.reshape(np.array(T_out, dtype=np.float32), len(T_out))
        T_file.close()

        I_r_file = open(rad_file)
        I_csvreader = csv.reader(I_r_file)
        next(I_csvreader)
        I_r = []
        for row in I_csvreader:
            I_r.append(row)
        I_r = np.reshape(np.array(I_r, dtype=np.float32), len(I_r))
        I_r_file.close()

        sun_ang_file = open(angle_file)
        angle_csvreader = csv.reader(sun_ang_file)
        next(angle_csvreader)
        sun_angle = []
        for row in angle_csvreader:
            sun_angle.append(row)
        sun_angle = np.reshape(np.array(sun_angle, dtype=np.float32), len(sun_angle))
        sun_angle = np.deg2rad(sun_angle)
        sun_ang_file.close()


        return T_out, I_r, sun_angle



    def update_window(self, size : int):
        """
        compute new heat balance after update

        :param size: window size
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        self.size = size
        heat_calculations = self.compute_heat_balance()

        return heat_calculations
        

    def update_isolation(self, width : int ):
        """
        compute new heat balance after update
        
        :param width: isolation width
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        self.isolation = width
        heat_calculations = self.compute_heat_balance()

        return heat_calculations

    def update_orientation(self, degree : int):
        """
        compute new heat balance after update
        
        :param size: building orientation
        :return: HeatBalance (object describing heat balance of the buidling)
        """
        self.degree = degree
        heat_calculations = self.compute_heat_balance()

        return heat_calculations

    # def compute_heat_balance(self):


    #     months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    #     month_temp_idx = [1, 745, 1415, 2161, 2881, 3625, 4345, 5089, 5833, 6553, 7297, 8017, 8760]
    #     heat_calculations = {}

    #     A_wall = (1-self.size)*100 # m^2, Wall surface area in contact with outside
    #     A_wind = 100*self.size
    #     A_wall_exposed = A_wall/4 * math.cos(np.deg2rad(self.degree)) + A_wall/4 * math.sin(np.deg2rad(self.degree))
    #     A_wind_exposed = A_wind/4 * math.cos(np.deg2rad(self.degree)) + A_wind/4 * math.sin(np.deg2rad(self.degree))
    #     #T_out, I_r, sun_angle = self.read_data('Temp_Data_Basel_2021.csv', 'Radiation_Data_Zurich_2018.csv', 'Zenith_Angle_Data_Zurich_2018.csv')
    #     #Solar Radiation through window
    #     T_out = self.T_out
    #     I_r = self.I_r
    #     sun_angle = self.sun_angle
    #     z = 0.68 # Shading coefficient
    #     ws = 1 #Radiation transmittance coefficient
    #     #Solar radiation absorbed by outer wall

    #     Eps_s = 0.6

    #     #Conduction
    #     J2kwh = 2.77778 * 10 ** (-7)  # Conversion coefficient between J and kWh
    #     Th_cond_wall = 1.2  # W/m/K, concrecte wall themrla Conductivity
    #     Th_cond_window = 0.7
    #     e_window= 0.1
    #     timestep = 60*60 #1-hour
    #     air_coeff = 3

    #     for i in range(0, len(months)):

    #         Q_wall = abs(np.multiply(Eps_s * A_wall_exposed*I_r[month_temp_idx[i]:month_temp_idx[i+1]], np.cos(sun_angle[month_temp_idx[i]:month_temp_idx[i+1]])))
    #         T_we = np.divide(Q_wall+Th_cond_wall/self.isolation * A_wall * self.int_temp + air_coeff*A_wall*T_out[month_temp_idx[i]:month_temp_idx[i+1]], Th_cond_wall/self.isolation * A_wall+air_coeff*A_wall)
    #         #Q_loss = Th_cond_wall/self.isolation * A_wall * (T_out[month_temp_idx[i]:month_temp_idx[i+1]] - self.int_temp) + Th_cond_window/e_window * A_wind *(T_out[month_temp_idx[i]:month_temp_idx[i+1]] - self.int_temp)
    #         Q_loss = Th_cond_wall/self.isolation * A_wall * (T_we - self.int_temp) + Th_cond_window/e_window * A_wind *(T_we - self.int_temp)
    #         Q_sun = abs(np.multiply(z*ws*I_r[month_temp_idx[i]:month_temp_idx[i+1]],np.cos(sun_angle[month_temp_idx[i]:month_temp_idx[i+1]])*A_wind_exposed))
    #         E_loss_cond = 0
    #         E_sun = 0
    #         for j in range (0, len(Q_loss)-1):
    #             E_loss_cond = E_loss_cond+(Q_loss[j]+Q_loss[j+1])/2 * timestep
    #             E_sun = E_sun + (Q_sun[j]+Q_sun[j+1])/2 * timestep
    #         E_loss_cond *= J2kwh
    #         E_sun  *= J2kwh
    #         E_heat = -(E_loss_cond+E_sun)
    #         heat_calculations[months[i]] = HeatBalanceMonth(E_sun/100.0,E_heat/100.0,E_loss_cond/100.0)
    #     return HeatBalance(heat_calculations)



    def compute_heat_balance(self):
        days_per_week = int(len(self.T_out)/(48*24))
        heat_calculations = []
        A_wall = (1-self.size)*3.6*3.0 # m^2, Wall surface area in contact with outside
        A_wind = 3.6*3.0*self.size
        #A_wall_exposed = A_wall * math.cos(np.deg2rad(self.degree)) + A_wall * math.sin(np.deg2rad(self.degree))
        A_wind_exposed = A_wind * math.sin(np.deg2rad(self.degree))# #+ A_wind * math.sin(np.deg2rad(self.degree))
        #Solar Radiation through window
        T_out = self.T_out
        I_r = self.I_r
        sun_angle = self.sun_angle
        z = 0.68 # Shading coefficient
        ws = 1 #Radiation transmittance coefficient
        #Solar radiation absorbed by outer wall
        Eps_s = 0.6

        #Conduction
        J2kwh = 2.77778 * 10 ** (-7)  # Conversion coefficient between J and kWh
        Th_cond_wall = 0.2  # W/m/K, concrecte wall themrla Conductivity
        Th_cond_window = 1.7
        e_window= 0.1
        timestep = 60*60 #1-hour
        for i in range(0, 48):
            #Q_wall = abs(np.multiply(Eps_s * A_wall_exposed*I_r[24*i*days_per_week:24*(i+1)*days_per_week], np.cos(sun_angle[24*i*days_per_week:24*(i+1)*days_per_week])))
            #T_we = np.divide(Q_wall+Th_cond_wall/self.isolation * A_wall * self.int_temp + air_coeff*A_wall*T_out[month_temp_idx[i]:month_temp_idx[i+1]], Th_cond_wall/self.isolation * A_wall+air_coeff*A_wall)
            Q_loss = Th_cond_wall/self.isolation * A_wall * (T_out[24*i*days_per_week:24*(i+1)*days_per_week] - self.int_temp) + Th_cond_window/e_window * A_wind *(T_out[24*i*days_per_week:24*(i+1)*days_per_week] - self.int_temp)
            Q_sun = abs(np.multiply(z*ws*I_r[24*i*days_per_week:24*(i+1)*days_per_week], np.cos(sun_angle[24*i*days_per_week:24*(i+1)*days_per_week])*A_wind_exposed))
            
            
            for j in range(0,days_per_week):
                if self.degree >=5 and self.degree<=195:
                    Q_sun[j*24+12:(j+1)*24] /= 2
                #else:
                 #   Q_sun[j*24:j*24+12] = 0
            
            
            E_loss_cond = 0
            E_sun = 0
            for j in range (0, len(Q_loss)-1):
                E_loss_cond = E_loss_cond+(Q_loss[j]+Q_loss[j+1])/2 * timestep
                E_sun = E_sun + (Q_sun[j]+Q_sun[j+1])/2 * timestep
            E_loss_cond *= J2kwh
            E_sun  *= J2kwh
            E_heat = -(E_loss_cond+E_sun)
            heat_calculations.append(HeatBalanceWeek(E_sun/16.2,E_heat/16.2,E_loss_cond/16.2))
        return HeatBalance(heat_calculations)
        #return heat_calculations

# test_class = ConductionModel()


# test_values = test_class.update_isolation(0.3)

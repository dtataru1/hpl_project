
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure




## TODO end implementation heat balance
class HeatBalanceWeek():
    def __init__(self, solarGain, heaterGain, heatLoss):
        self.solarGain = solarGain
        self.heaterGain = heaterGain
        self.heatLoss = heatLoss

class HeatBalanceMonth():

    def __init__(self, solarGain, heaterGain, heatLoss):
        self.solarGain = solarGain
        self.heaterGain = heaterGain
        self.heatLoss = heatLoss

class HeatBalance():

    def __init__(self, WeeklyHeatConsumption=None):
        self.WeeklyHeatConsumption = WeeklyHeatConsumption
        if WeeklyHeatConsumption is None:
            self.defaultConsumption()

    def _defaultConsumption(self):
        self.WeeklyHeatConsumption = [HeatBalanceWeek(1,4,2), HeatBalanceWeek(2,3,1), HeatBalanceWeek(5,2,1)]


# class HeatBalance():
    
#     def __init__(self, monthlyHeatconsumption=None):
#         self.monthlyHeatconsumption = monthlyHeatconsumption
#         if monthlyHeatconsumption is None :
#             self._defaultConsumption()
        
#     def _defaultConsumption(self):
#         self.monthlyHeatconsumption = {'January' : HeatBalanceMonth(2,5,7), 
#             'February' : HeatBalanceMonth(2,8,10), 
#             'March' : HeatBalanceMonth(2,4,6)}


class HeatBalanceGraph(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#f0f0f0')
        self.axsMonths, self.axsTot = fig.subplots(1,2, gridspec_kw={'width_ratios': [5, 1]})
        self.months = ['jan', 'fev', 'mars', 'avril', 'mai', 'juin', 'jui', 'aout','sept', 'oct', 'nov', 'dec']
        super(HeatBalanceGraph, self).__init__(fig)
    
    def remove_frames(self, axs):
        axs.spines['top'].set_visible(False)
        axs.spines['right'].set_visible(False)

    
    def plot(self, heatBalance):
        self.axsMonths.cla()
        self.axsTot.cla()
        #consumption = heatBalance.monthlyHeatconsumption.values()
        #labels = heatBalance.monthlyHeatconsumption.keys()
        consumption = heatBalance.WeeklyHeatConsumption
        indices =  list(range(48))
        ### TO DO : use colorblind palette improve the pallete
        ### TO DO : improve display
      
      
        goodSolarGain = extract_gain(consumption, lambda h : h.solarGain)
        badSolarGain = extract_gain(consumption, lambda h : min(0,h.heaterGain))
        heaterGain = extract_gain(consumption, lambda h : max(0,h.heaterGain))
        airCooling = extract_gain(consumption, lambda h : min(0,h.heaterGain))
        heatLoss = extract_gain(consumption, lambda h : min(0,h.heatLoss))

       
       

        tot_heatLoss = [sum(heaterGain)]
        

        #self.axsTot.bar([1],tot_aircooling, color='#3ec1c3')
        self.axsTot.bar([1],tot_heatLoss, color='#ef4a5a')
        self.axsTot.set_title('consomation annuel')
        self.axsTot.plot([0.5, 1.5], [149, 149], color='black', label='consomation moyenne')
        self.axsTot.plot([0.5, 1.5], [41, 41], color='#a2c616', label='minergie')
        self.remove_frames(self.axsTot)
        self.axsTot.set_xticks([])
        self.axsTot.set_ylabel('kwH/m²')
        self.axsTot.set_ylim([0,350])
        self.axsTot.legend()


        labels = [self.months[i//4] if i%4==1 else '' for i in range(48)]
        self.axsMonths.bar(indices, heaterGain, bottom=goodSolarGain, color='#ef4a5a', label='chauffage', tick_label=labels)
        
        self.axsMonths.bar(indices, goodSolarGain, color='#ffd11c', label='gain solaire', tick_label=labels)
        self.axsMonths.bar(indices, badSolarGain, color='#3ec1c3', label='gain solaire non voulu', tick_label=labels)
        
        #self.axsMonths.bar(indices, airCooling,color='#3ec1c3', label='climatisation', tick_label=labels)
        #self.axsMonths.bar(indices, heatLoss, bottom=airCooling, color='#7e7e85', label='perte thermique', tick_label=labels)
        self.axsMonths.set_xticks([])
        self.axsMonths.set_xticklabels([str(4*i+1) for i in range(12)])
        self.remove_frames(self.axsMonths)

        self.axsMonths.set_xticks(indices)
        self.axsMonths.set_xticklabels(labels)
        self.axsMonths.set_ylim([-30,45])
        self.axsMonths.set_title('consomation par mois')
        self.axsMonths.set_ylabel('kwH/m²')
        self.axsMonths.legend()


        self.draw()

def extract_gain(ls, extract):
    return list(map(extract, ls))

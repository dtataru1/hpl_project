
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


## TODO end implementation heat balance
class HeatBalanceMonth():

    def __init__(self, solarGain, heaterGain, heatLoss):
        self.solarGain = solarGain
        self.heaterGain = heaterGain
        self.heatLoss = heatLoss


class HeatBalance():
    
    def __init__(self, monthlyHeatconsumption=None):
        self.monthlyHeatconsumption = monthlyHeatconsumption
        if monthlyHeatconsumption is None :
            self._defaultConsumption()
        
    def _defaultConsumption(self):
        self.monthlyHeatconsumption = {'January' : HeatBalanceMonth(2,5,7), 
            'February' : HeatBalanceMonth(2,8,10), 
            'March' : HeatBalanceMonth(2,4,6)}

class HeatBalanceGraph(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axs = fig.add_subplot(111)
        super(HeatBalanceGraph, self).__init__(fig)
    
    def plot(self, heatBalance):
        self.axs.cla()
        consumption = heatBalance.monthlyHeatconsumption.values()
        labels = heatBalance.monthlyHeatconsumption.keys()
        indices =  np.arange(len(labels))
        ### TO DO : use colorblind palette improve the pallete
        ### TO DO : improve display
      
      
        solarGain = extract_gain(consumption, lambda h : h.solarGain)
        heaterGain = extract_gain(consumption, lambda h : max(0,h.heaterGain))
        airCooling = extract_gain(consumption, lambda h : min(0,h.heaterGain))
        heatLoss = extract_gain(consumption, lambda h : h.heatLoss)

        self.axs.bar(indices, heaterGain, color='#ef4a5a', label='chauffage')
        self.axs.bar(indices, solarGain, bottom=heaterGain,color='#ffd11c', label='gain solaire')
        self.axs.bar(indices, airCooling,color='#3ec1c3', label='climatisation')
        self.axs.bar(indices, heatLoss, bottom=airCooling, color='#7e7e85', label='perte thermique')
        self.axs.set_xticks(indices)
        self.axs.set_xticklabels(labels)
        self.axs.legend()
        self.draw()

def extract_gain(ls, extract):
    return list(map(extract, ls))

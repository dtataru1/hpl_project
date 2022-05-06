
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
        fig.patch.set_facecolor('#f0f0f0')
        self.axsMonths, self.axsTot = fig.subplots(1,2, gridspec_kw={'width_ratios': [5, 1]})
        super(HeatBalanceGraph, self).__init__(fig)
    
    def remove_frames(self, axs):
        axs.spines['top'].set_visible(False)
        axs.spines['right'].set_visible(False)

    
    def plot(self, heatBalance):
        self.axsMonths.cla()
        self.axsTot.cla()
        consumption = heatBalance.monthlyHeatconsumption.values()
        labels = heatBalance.monthlyHeatconsumption.keys()
        indices =  np.arange(len(labels))
        ### TO DO : use colorblind palette improve the pallete
        ### TO DO : improve display
      
      
        solarGain = extract_gain(consumption, lambda h : h.solarGain)
        heaterGain = extract_gain(consumption, lambda h : max(0,h.heaterGain))
        airCooling = extract_gain(consumption, lambda h : min(0,h.heaterGain))
        heatLoss = extract_gain(consumption, lambda h : h.heatLoss)

        tot_heatLoss = [-sum(heatLoss)]
        tot_aircooling = [-sum(airCooling)]
        self.axsTot.bar([1],tot_aircooling, color='#3ec1c3')
        self.axsTot.bar([1],tot_heatLoss, bottom=tot_aircooling, color='#7e7e85')
        self.axsTot.set_title('consomation annuel')
        self.axsTot.plot([0.5, 1.5], [149, 149], color='black', label='consomation moyenne')
        self.axsTot.plot([0.5, 1.5], [41, 41], color='#a2c616', label='minergie')
        self.remove_frames(self.axsTot)
        self.axsTot.set_xticks([])
        self.axsTot.legend()


        self.axsMonths.bar(indices, heaterGain, color='#ef4a5a', label='chauffage')
        self.axsMonths.bar(indices, solarGain, bottom=heaterGain,color='#ffd11c', label='gain solaire')
        self.axsMonths.bar(indices, airCooling,color='#3ec1c3', label='climatisation')
        self.axsMonths.bar(indices, heatLoss, bottom=airCooling, color='#7e7e85', label='perte thermique')
        self.remove_frames(self.axsMonths)

        self.axsMonths.set_xticks(indices)
        self.axsMonths.set_xticklabels(labels)
        self.axsMonths.set_title('consomation par mois')
        self.axsMonths.legend()


        self.draw()

def extract_gain(ls, extract):
    return list(map(extract, ls))

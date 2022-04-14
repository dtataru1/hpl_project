import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class HeatBalance():
    
    def __init__(self, monthlyHeatconsumption=None):
        self.monthlyHeatconsumption = monthlyHeatconsumption
        self._defaultConsumption()
        
    def _defaultConsumption(self):
        self.monthlyHeatconsumption = {'January' : 10, 'February' : 5, 'March' : 2}

class HeatBalanceGraph(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axs = fig.add_subplot(111)
        super(HeatBalanceGraph, self).__init__(fig)
    
    def plot(self, heatBalance):
        self.axs.cla()
        consumption = heatBalance.monthlyHeatconsumption.values()
        labels = heatBalance.monthlyHeatconsumption.keys()
        print(labels)
        indices =  np.arange(3)
        self.axs.bar(indices, consumption, color='red')
        self.axs.set_xticks(indices)
        self.axs.set_xticklabels(labels)
        self.draw()
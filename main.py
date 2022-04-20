from PyQt5 import QtCore, QtWidgets
import sys
from createWindow import create_window
from conduction import ConductionModel
from heatBalance import HeatBalanceGraph, HeatBalance

class Window(QtWidgets.QMainWindow):
    def __init__(self, graph, conduction_model, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.conduction_model = conduction_model

        self.window_silder, self.isolation_slider, self.orientation_dial = create_window(self, graph)

        self.window_silder.valueChanged['int'].connect(lambda x: self.update_window(x))
        self.isolation_slider.valueChanged['int'].connect(lambda x: self.update_isolation(x))
        self.orientation_dial.valueChanged['int'].connect(lambda x: self.update_orientation(x))
        self.show()

    

    def update_window(self, size):
        pass

    def update_isolation(self, size):
        pass

    def update_orientation(self, degree):
        pass



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    
    heat_balance_graph = HeatBalanceGraph()
    conduction_model = ConductionModel(heat_balance_graph)

    main_window = Window(heat_balance_graph, conduction_model) 
    heat_balance_graph.plot(HeatBalance())
    sys.exit(app.exec())
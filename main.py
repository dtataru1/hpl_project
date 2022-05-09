from PyQt5 import QtCore, QtWidgets
import sys
from conduction import ConductionModel
from heatBalance import HeatBalanceGraph, HeatBalance
from window import Window





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    
    heat_balance_graph = HeatBalanceGraph()
    conduction_model = ConductionModel()
    
    main_window = Window(heat_balance_graph, conduction_model, size)
    heat_balance_graph.plot(HeatBalance())
    sys.exit(app.exec())
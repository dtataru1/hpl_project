from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtWidgets
from heatBalance import HeatBalance
from heat_loss_graphing import Ui_Form



class Window(QtWidgets.QMainWindow):
    """
        Window main window of our application
    """
    def __init__(self, graph, conduction_model, parent=None):
        """
        Construct the main window.
        Initialize all visual components

        :param graph: the consumption graph
        :param conduction_model: the conduction model
        :return: returns nothing
        """
        super().__init__(parent)
        self.graph = graph
        self.conduction_model = conduction_model

        ## we shall always use the graph instead of canvas
        ## we shall always return the controlls buttons

        self.window_silder, self.isolation_slider, self.orientation_dial = Ui_Form().setupUi(self, graph)

        ## do not touch
        self.window_silder.valueChanged['int'].connect(lambda x: self.update_window(x))
        self.isolation_slider.valueChanged['int'].connect(lambda x: self.update_isolation(x))
        self.orientation_dial.valueChanged['int'].connect(lambda x: self.update_orientation(x))
        self.show()

    

    def update_window(self, size : int):
        """
        update conduction model and UI when the window size is updated
        :param size: window size
        """
        heatBalance = self.conduction_model.update_window(size)
        self.graph.plot(heatBalance) 

    def update_isolation(self, size : int):
        """
        update conduction model and UI when the isolation width is updated
        :param size: isolation width
        """
        heatBalance = self.conduction_model.update_isolation(size)
        self.graph.plot(heatBalance)

    def update_orientation(self, degree : int):
        """
        update conduction model and UI when the building orientation is updated
        :param degree: building orientation
        """
        heatBalance = self.conduction_model.update_orientation(degree)
        self.graph.plot(heatBalance)




    
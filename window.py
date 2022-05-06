from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtWidgets
from heatBalance import HeatBalance
from Heat_loss_graphing import Ui_Form


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

        # Prompts setup
        text = open('prompts.txt', 'r')
        self.prompts = text.readlines()
        text.close()
        self.prompts_count = len(self.prompts)
        self.current_prompt = 0

        ## we shall always use the graph instead of canvas
        ## we shall always return the controlls buttons

        self.window_slider, self.isolation_slider, self.orientation_dial, self.previous_prompt, self.next_prompt, \
        self.prompt_text = Ui_Form().setupUi(self, graph)

        self.previous_prompt.clicked.connect(self.backward_prompt)
        self.next_prompt.clicked.connect(self.forward_prompt)
        ## do not touch
        
        self.window_slider.valueChanged['int'].connect(lambda x: self.update_window(x/self.window_slider.maximum()))
        self.isolation_slider.valueChanged['int'].connect(lambda x: self.update_isolation(x/self.isolation_slider.maximum()))
        self.orientation_dial.valueChanged['int'].connect(lambda x: self.update_orientation(360*x/self.orientation_dial.maximum()))
        self.show()

    def forward_prompt(self):
        if self.current_prompt < self.prompts_count - 1:
            self.current_prompt += 1
            self.prompt_text.setText(self.prompts[self.current_prompt])

    def backward_prompt(self):
        if self.current_prompt > 0:
            self.current_prompt -= 1
            self.prompt_text.setText(self.prompts[self.current_prompt])

    def update_window(self, size: float):
        """
        update conduction model and UI when the window size is updated
        :param size: window size
        """
        heatBalance = self.conduction_model.update_window(size)
        self.graph.plot(heatBalance)

    def update_isolation(self, size: float):
        """
        update conduction model and UI when the isolation width is updated
        :param size: isolation width
        """
        heatBalance = self.conduction_model.update_isolation(size)
        self.graph.plot(heatBalance)

    def update_orientation(self, degree: float):
        """
        update conduction model and UI when the building orientation is updated
        :param degree: building orientation
        """
        heatBalance = self.conduction_model.update_orientation(degree)
        self.graph.plot(heatBalance)

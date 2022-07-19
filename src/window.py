from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtWidgets
from heatBalance import HeatBalance
from Heat_loss_graphing import Ui_Form
import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg


class Window(QtWidgets.QMainWindow):
    """
        Window main window of our application
    """

    def __init__(self, graph, conduction_model, size, parent=None):
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
        text = open('prompts.txt', 'r', encoding='utf-8')
        self.prompts = text.readlines()
        text.close()
        self.prompts_count = len(self.prompts)
        self.current_prompt = 0

        ## we shall always use the graph instead of canvas
        ## we shall always return the controlls buttons

        self.window_slider, self.isolation_slider, self.orientation_dial, self.previous_prompt, self.next_prompt, \
        self.prompt_text, self.isolation_print, self.windows_print, self.orientation_print, self.image = Ui_Form().setupUi(self, graph, size)

        self.previous_prompt.clicked.connect(self.backward_prompt)
        self.next_prompt.clicked.connect(self.forward_prompt)
        ## do not touch
        
        self.window_slider.valueChanged['int'].connect(lambda x: self.update_window(x/self.window_slider.maximum()))
        self.isolation_slider.valueChanged['int'].connect(lambda x: self.update_isolation(0.4*x/self.isolation_slider.maximum()))
        self.orientation_dial.valueChanged['int'].connect(lambda x: self.update_orientation(360*x/self.orientation_dial.maximum()))
        self.show()

    def forward_prompt(self):
        if self.current_prompt < self.prompts_count - 1:
            self.current_prompt += 1
            self.prompt_text.setText(self.prompts[self.current_prompt])
            self.prompt_text.setScaledContents(True)

    def backward_prompt(self):
        if self.current_prompt > 0:
            self.current_prompt -= 1
            self.prompt_text.setText(self.prompts[self.current_prompt])
            self.prompt_text.setScaledContents(True)

    def update_window(self, size: float):
        """
        update conduction model and UI when the window size is updated
        :param size: window size
        """
        self.windows_print.setText("%.0f %%" % (size*100))
        heatBalance = self.conduction_model.update_window(size)
        self.graph.plot(heatBalance)
        self.update_image(self.image, self.isolation_slider.value()/100, size)

    def update_isolation(self, size: float):
        """
        update conduction model and UI when the isolation width is updated
        :param size: isolation width
        """
        self.isolation_print.setText("%.1f cm" % (size*100))
        heatBalance = self.conduction_model.update_isolation(size)
        self.graph.plot(heatBalance)
        self.update_image(self.image, size, self.window_slider.value()/100)

    def update_orientation(self, degree: float):
        """
        update conduction model and UI when the building orientation is updated
        :param degree: building orientation
        """
        self.orientation_print.setText("%.0f °" % degree)
        heatBalance = self.conduction_model.update_orientation(degree)
        self.graph.plot(heatBalance)

    def update_image(self, image, isolation_size, window_size):
        # Clear image
        image.clear()
        c = pg.glColor(0, 0, 0, 100)
        # Fixed frame
        points_fixed = np.array([[1.8, 0, 1.5], [1.8, 0, -1.5], [-1.8, 0, -1.5], [-1.8, 0, 1.5], [1.8, 0, 1.5]])
        fixed_frame = gl.GLLinePlotItem(pos=points_fixed, mode='line_strip', color=c, glOptions='translucent')
        image.addItem(fixed_frame)

        # Window frame
        points_window = points_fixed * np.sqrt(window_size)
        window_frame = gl.GLLinePlotItem(pos=points_window, mode='line_strip', color=c, glOptions='translucent')
        image.addItem(window_frame)

        # Depth
        frame_depth_points = np.empty((8, 3))
        frame_depth_points[0::2, ] = points_fixed[:4, ]
        frame_depth_points[1::2, ] = points_fixed[:4, ] + isolation_size * np.array(
            [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
        frame_depth = gl.GLLinePlotItem(pos=frame_depth_points, mode='lines', color=c, glOptions='translucent')
        image.addItem(frame_depth)

        if window_size != 0:
            window_depth_points = np.empty((8, 3))
            window_depth_points[0::2, ] = points_window[:4, ]
            window_depth_points[1::2, ] = points_window[:4, ] + isolation_size * np.array(
                [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
            window_depth = gl.GLLinePlotItem(pos=window_depth_points, mode='lines', color=c, glOptions='translucent')
            image.addItem(window_depth)

        # Back frame
        back_points = points_fixed + isolation_size * np.array(
            [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
        back_frame = gl.GLLinePlotItem(pos=back_points, mode='line_strip', color=c, glOptions='translucent')
        image.addItem(back_frame)

        back_window_points = points_window + isolation_size * np.array(
            [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
        back_window_frame = gl.GLLinePlotItem(pos=back_window_points, mode='line_strip', color=c, glOptions='translucent')
        image.addItem(back_window_frame)

        # Labels
        hoffset = -1.9
        voffset = 1.6
        spacing = -.15
        centering = (5 * spacing + .1) / 2

        three_points = np.array([[0, 0, 0], [-.1, 0, 0], [-.1, 0, .1], [0, 0, .1], [-.1, 0, .1],
                                 [-.1, 0, .2], [0, 0, .2]])
        three = gl.GLLinePlotItem(pos=three_points + np.array([[hoffset, 0, 0]] * 7), mode='line_strip', color=c,
                                  glOptions='translucent')
        self.image.addItem(three)

        zero_points = np.array([[0, 0, 0], [-.1, 0, 0], [-.1, 0, .2], [0, 0, .2], [0, 0, 0]])
        zero = gl.GLLinePlotItem(pos=zero_points + np.array([[hoffset + spacing, 0, 0]] * 5), mode='line_strip',
                                 color=c, glOptions='translucent')
        self.image.addItem(zero)

        zero_2 = gl.GLLinePlotItem(pos=(zero_points + np.array([[hoffset + 2 * spacing, 0, 0]] * 5)), mode='line_strip',
                                   color=c,
                                   glOptions='translucent')
        self.image.addItem(zero_2)

        letter_c_points = np.array([[0, 0, 0], [.1, 0, 0], [.1, 0, .1], [0, 0, .1]])
        letter_c = gl.GLLinePlotItem(pos=letter_c_points + np.array([[hoffset + 4 * spacing, 0, 0]] * 4),
                                     mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(letter_c)

        letter_m_points = np.array(
            [[0, 0, 0], [0, 0, .1], [.05, 0, .1], [.05, 0, 0], [.05, 0, .1], [.1, 0, .1], [.1, 0, 0]])
        letter_m = gl.GLLinePlotItem(pos=letter_m_points + np.array([[hoffset + 5 * spacing, 0, 0]] * 7),
                                     mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(letter_m)

        three_up = gl.GLLinePlotItem(pos=three_points + np.array([[-centering, 0, voffset]] * 7), mode='line_strip',
                                     color=c, glOptions='translucent')
        self.image.addItem(three_up)

        six_points = np.array([[-.1, 0, .2], [0, 0, .2], [0, 0, 0], [-.1, 0, 0], [-.1, 0, .1], [0, 0, .1]])
        six_up = gl.GLLinePlotItem(pos=six_points + np.array([[spacing - centering, 0, voffset]] * 6),
                                   mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(six_up)

        zero_up = gl.GLLinePlotItem(pos=zero_points + np.array([[2 * spacing - centering, 0, voffset]] * 5),
                                    mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(zero_up)

        letter_c_up = gl.GLLinePlotItem(pos=letter_c_points + np.array([[4 * spacing - centering, 0, voffset]] * 4),
                                        mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(letter_c_up)

        letter_m_up = gl.GLLinePlotItem(pos=letter_m_points + np.array([[5 * spacing - centering, 0, voffset]] * 7),
                                        mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(letter_m_up)
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Parameters.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import matplotlib
import numpy as np
import csv
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

class QImageViewer(QtWidgets.QMainWindow):
    def __init__(self,sizeh,sizev,img):
        super().__init__()

        self.scaleFactor = 0.0

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)


        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        #self.createMenus()

        self.setWindowTitle("Théorie")
        self.resize(sizeh, sizev)

        self.imageLabel.setPixmap(QtGui.QPixmap(img).scaledToWidth(sizeh-36))
        self.scaleFactor = 1.0

        self.scrollArea.setVisible(True)
        self.printAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()


    def open(self):
        options = QtWidgets.QFileDialog.Options()
        # fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'QtWidgets.QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            #self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>The <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p>")

    def createActions(self):
        self.openAct = QtWidgets.QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QtWidgets.QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QtWidgets.QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QtWidgets.QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QtWidgets.QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QtWidgets.QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)
        self.aboutAct = QtWidgets.QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QtWidgets.QAction("About &Qt", self, triggered=QtWidgets.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QtWidgets.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QtWidgets.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QtWidgets.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, ybound=(-1000, 0))
        super(MplCanvas, self).__init__(fig)


class Ui_Form(object):

    def setupUi(self, Form, graph, size):
        Form.setObjectName("Form")
        Form.setStyleSheet("QLabel{font-size: 9pt;}")
        width = size.width()
        height = size.height()
        Form.resize(width, height)

        margin = width / 50
        vskip = height / 36
        # PARAMETERS

        self.label_parameters = QtWidgets.QLabel(Form)
        self.label_parameters.setGeometry(QtCore.QRect(margin, margin, width / 4, 20))
        self.label_parameters.setObjectName("label_parameters")

        # Isolation
        self.label_isolation = QtWidgets.QLabel(Form)
        self.label_isolation.setGeometry(QtCore.QRect(margin, margin + 2 * vskip, width / 4, 30))
        self.label_isolation.setObjectName("label_isolation")

        self.slider_isolation = QtWidgets.QSlider(Form)
        self.slider_isolation.setGeometry(QtCore.QRect(margin, margin + 3 * vskip, width / 4 - 3 * vskip, 30))
        self.slider_isolation.setOrientation(QtCore.Qt.Horizontal)
        self.slider_isolation.setMinimum(1)
        self.slider_isolation.setMaximum(80)
        self.slider_isolation.setValue(10)
        self.slider_isolation.setObjectName("slider_isolation")
        self.slider_isolation.setDisabled(True)

        self.isolation_print = QtWidgets.QLabel(Form)
        self.isolation_print.setGeometry(
            QtCore.QRect(margin + width / 4 - 2 * vskip, margin + 3 * vskip, 3 * vskip, 30))
        self.isolation_print.setObjectName("isolation_print")

        # Windows
        self.label_windows = QtWidgets.QLabel(Form)
        self.label_windows.setGeometry(QtCore.QRect(margin, margin + 5 * vskip, width / 4, 30))
        self.label_windows.setObjectName("label_windows")

        self.slider_windows = QtWidgets.QSlider(Form)
        self.slider_windows.setGeometry(QtCore.QRect(margin, margin + 6 * vskip, width / 4 - 3 * vskip, 30))
        self.slider_windows.setOrientation(QtCore.Qt.Horizontal)
        self.slider_windows.setObjectName("slider_windows")
        self.slider_windows.setValue(20)
        self.slider_windows.setDisabled(True)

        self.windows_print = QtWidgets.QLabel(Form)
        self.windows_print.setGeometry(QtCore.QRect(margin + width / 4 - 2 * vskip, margin + 6 * vskip, 3 * vskip, 30))
        self.windows_print.setObjectName("isolation_print")

        # Orientation
        self.label_orientation = QtWidgets.QLabel(Form)
        self.label_orientation.setGeometry(QtCore.QRect(margin, margin + 8 * vskip, width / 4, 30))
        self.label_orientation.setObjectName("label_orientation")

        self.dial_orientation = QtWidgets.QDial(Form)
        self.dial_orientation.setWrapping(True)
        self.dial_orientation.setGeometry(QtCore.QRect(margin + width / 12, margin + 9 * vskip, width / 12, width / 12))
        self.dial_orientation.setObjectName("dial_orientation")
        self.dial_orientation.setMinimum(0)
        self.dial_orientation.setMaximum(359)
        self.dial_orientation.setValue(270)
        self.dial_orientation.setDisabled(True)

        self.orientation_print = QtWidgets.QLabel(Form)
        self.orientation_print.setGeometry(QtCore.QRect(margin+width/12+width/36,margin+9*vskip+width/36,width/36,width/36))
        self.orientation_print.setAlignment(QtCore.Qt.AlignCenter)
        self.orientation_print.setObjectName("orientation_print")

        self.label_north = QtWidgets.QLabel(Form)
        self.label_north.setGeometry(QtCore.QRect(margin + width / 12, margin + 9 * vskip - 30, width / 12, 30))
        self.label_north.setAlignment(QtCore.Qt.AlignCenter)
        self.label_north.setObjectName("label_windows_2")

        self.label_south = QtWidgets.QLabel(Form)
        self.label_south.setGeometry(
            QtCore.QRect(margin + width / 12, margin + 9 * vskip - 30 + width / 12 + 30, width / 12, 30))
        self.label_south.setAlignment(QtCore.Qt.AlignCenter)
        self.label_south.setObjectName("label_south")

        self.label_west = QtWidgets.QLabel(Form)
        self.label_west.setGeometry(QtCore.QRect(margin + width / 12 - 30, margin + 9 * vskip, 30, width / 12))
        self.label_west.setAlignment(QtCore.Qt.AlignCenter)
        self.label_west.setObjectName("label_west")

        self.label_east = QtWidgets.QLabel(Form)
        self.label_east.setGeometry(QtCore.QRect(margin + 2 * width / 12, margin + 9 * vskip, 30, width / 12))
        self.label_east.setAlignment(QtCore.Qt.AlignCenter)

        self.label_east.setObjectName("label_east")

        # Placeholder for graph
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(2 * margin + width / 4, 2 * margin + height / 6, 2 * width / 3, 2 * height / 3)
        layout = QtWidgets.QVBoxLayout(self.widget)

        # Graph object
        self.canvas = graph
        layout.addWidget(self.canvas)
        # self.canvas.setGeometry(QtCore.QRect(200, 0, 900, 600))

        # Text object: questions, explanations, etc.
        self.prompt_text = QtWidgets.QLabel(Form)
        self.prompt_text.setGeometry(
            QtCore.QRect(2 * margin + width / 4, 2 * margin + width / 40, 2 * width / 3, height / 6 - width / 40))
        self.prompt_text.setObjectName("prompt_text")
        self.prompt_text.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt_text.setScaledContents(True)
        self.prompt_text.setWordWrap(True)
        self.prompt_text.setStyleSheet("border: 1px solid black; padding: 20px;")

        text = open('prompts.txt', 'r', encoding='utf-8')
        self.initial_prompt = text.readline()
        text.close()

        # Previous prompt button
        self.previous_button = QtWidgets.QToolButton(Form)
        self.previous_button.setArrowType(QtCore.Qt.LeftArrow)
        self.previous_button.setGeometry(QtCore.QRect(2 * margin + width / 4, margin, width / 40, width / 40))
        self.previous_button.setObjectName("previous_button")

        # Next prompt button
        self.next_button = QtWidgets.QToolButton(Form)
        self.next_button.setArrowType(QtCore.Qt.RightArrow)
        self.next_button.setGeometry(QtCore.QRect(2 * margin + width / 4 + width / 40, margin, width / 40, width / 40))
        self.next_button.setObjectName("next_button")

        # Theory buttons
        self.theory_button_1 = QtWidgets.QToolButton(Form)
        self.theory_button_1.setGeometry(
            QtCore.QRect(width / 4 + 2 * width / 3 - 3 * width / 40, margin, width / 40, width / 40))
        self.theory_button_1.setObjectName("theory_button_1")
        self.theory_button_1.setText("1")

        self.theory_button_2 = QtWidgets.QToolButton(Form)
        self.theory_button_2.setGeometry(
            QtCore.QRect(margin + width / 4 + 2 * width / 3 - 2 * width / 40, margin, width / 40, width / 40))
        self.theory_button_2.setObjectName("theory_button_2")
        self.theory_button_2.setText("2")

        self.theory_button_3 = QtWidgets.QToolButton(Form)
        self.theory_button_3.setGeometry(
            QtCore.QRect(2 * margin + width / 4 + 2 * width / 3 - width / 40, margin, width / 40, width / 40))
        self.theory_button_3.setObjectName("theory_button_3")
        self.theory_button_3.setText("3")

        # Theory displays

        self.theory_viewer_1 = QImageViewer(2/3*width,2/3*height,"conduction_theory.png")
        self.theory_viewer_2 = QImageViewer(2/3*width,2/3*height,"window_theory.png")
        self.theory_viewer_3 = QImageViewer(2/3*width,2/3*height,"angle_theory.png")
        # Connections
        self.theory_button_1.clicked.connect(self.theory_viewer_1.show)
        self.theory_button_1.clicked.connect(lambda: self.slider_isolation.setDisabled(False))

        self.theory_button_2.clicked.connect(self.theory_viewer_2.show)
        self.theory_button_2.clicked.connect(lambda: self.slider_windows.setDisabled(False))

        self.theory_button_3.clicked.connect(self.theory_viewer_3.show)
        self.theory_button_3.clicked.connect(lambda: self.dial_orientation.setDisabled(False))

        # Drawing stuff
        rem_vspace = height-(margin+9*vskip+width/12+30)
        space_available = min(width/4, rem_vspace)



        self.image = gl.GLViewWidget(Form)
        self.image.setGeometry(QtCore.QRect(margin, height-(rem_vspace-space_available)/2-space_available, space_available, space_available))
        self.image.setBackgroundColor(Form.palette().color(Form.backgroundRole()))
        self.image.opts['fov'] *= .8
        self.image.opts['distance'] *= .8
        self.image.show()
        c = pg.glColor(0, 0, 0, 100)

        # Fixed frame
        points_fixed = np.array([[1.8, 0, 1.5], [1.8, 0, -1.5], [-1.8, 0, -1.5], [-1.8, 0, 1.5], [1.8, 0, 1.5]])
        fixed_frame = gl.GLLinePlotItem(pos=points_fixed, mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(fixed_frame)

        # Window frame
        points_window = points_fixed * (np.sqrt(self.slider_windows.value() / 100))
        window_frame = gl.GLLinePlotItem(pos=points_window, mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(window_frame)

        # Depth
        frame_depth_points = np.empty((8, 3))
        frame_depth_points[0::2, ] = points_fixed[:4, ]
        frame_depth_points[1::2, ] = points_fixed[:4, ] + (self.slider_isolation.value() / 160) * np.array(
            [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
        frame_depth = gl.GLLinePlotItem(pos=frame_depth_points, mode='lines', color=c, glOptions='translucent')
        self.image.addItem(frame_depth)

        if self.slider_windows.value() != 0:
            window_depth_points = np.empty((8, 3))
            window_depth_points[0::2, ] = points_window[:4, ]
            window_depth_points[1::2, ] = points_window[:4, ] + (self.slider_isolation.value()/160) * np.array(
                [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
            window_depth = gl.GLLinePlotItem(pos=window_depth_points, mode='lines', color=c, glOptions='translucent')
            self.image.addItem(window_depth)

        # Back frame
        back_points = points_fixed + (self.slider_isolation.value() / 100) * np.array(
            [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
        back_frame = gl.GLLinePlotItem(pos=back_points, mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(back_frame)

        back_window_points = points_window + (self.slider_isolation.value() / 100) * np.array(
            [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
        back_window_frame = gl.GLLinePlotItem(pos=back_window_points, mode='line_strip', color=c,
                                              glOptions='translucent')
        self.image.addItem(back_window_frame)

        # Labels
        hoffset = -1.9
        voffset = 1.6
        spacing = -.15
        centering = (5*spacing+.1)/2

        three_points = np.array([[0, 0, 0], [-.1, 0, 0], [-.1, 0, .1], [0, 0, .1], [-.1, 0, .1],
                                 [-.1, 0, .2], [0, 0, .2]])
        three = gl.GLLinePlotItem(pos=three_points+np.array([[hoffset,0,0]]*7), mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(three)

        zero_points = np.array([[0, 0, 0], [-.1, 0, 0], [-.1, 0, .2], [0, 0, .2], [0, 0, 0]])
        zero = gl.GLLinePlotItem(pos=zero_points+np.array([[hoffset+spacing,0,0]]*5), mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(zero)

        zero_2 = gl.GLLinePlotItem(pos=(zero_points + np.array([[hoffset+2*spacing, 0, 0]] * 5)), mode='line_strip', color=c,
                                   glOptions='translucent')
        self.image.addItem(zero_2)

        letter_c_points = np.array([[0, 0, 0], [.1, 0, 0], [.1, 0, .1], [0, 0, .1]])
        letter_c = gl.GLLinePlotItem(pos=letter_c_points + np.array([[hoffset + 4 * spacing, 0, 0]] * 4), mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(letter_c)

        letter_m_points = np.array([[0, 0, 0], [0, 0, .1], [.05, 0, .1], [.05, 0, 0], [.05, 0, .1], [.1, 0, .1], [.1, 0, 0]])
        letter_m = gl.GLLinePlotItem(pos=letter_m_points + np.array([[hoffset + 5 * spacing, 0, 0]] * 7), mode='line_strip', color=c, glOptions='translucent')
        self.image.addItem(letter_m)

        three_up = gl.GLLinePlotItem(pos=three_points + np.array([[-centering,0,voffset]]*7),mode='line_strip',color=c,glOptions='translucent')
        self.image.addItem(three_up)

        six_points = np.array([[-.1,0,.2],[0,0,.2],[0,0,0],[-.1,0,0],[-.1,0,.1],[0,0,.1]])
        six_up = gl.GLLinePlotItem(pos=six_points + np.array([[spacing-centering,0,voffset]]*6),mode='line_strip',color=c,glOptions='translucent')
        self.image.addItem(six_up)

        zero_up = gl.GLLinePlotItem(pos=zero_points + np.array([[2*spacing-centering,0,voffset]]*5),mode='line_strip',color=c,glOptions='translucent')
        self.image.addItem(zero_up)

        letter_c_up = gl.GLLinePlotItem(pos=letter_c_points + np.array([[4*spacing-centering,0,voffset]]*4),mode='line_strip',color=c,glOptions='translucent')
        self.image.addItem(letter_c_up)

        letter_m_up = gl.GLLinePlotItem(pos=letter_m_points + np.array([[5*spacing-centering,0,voffset]]*7),mode='line_strip',color=c,glOptions='translucent')
        self.image.addItem(letter_m_up)


        # self.canvas.xdata = np.linspace(1,14,14)
        # self.canvas.ydata = np.zeros(14)
        # self.canvas.show()
        # self.window = 0
        # self.isolation = 0
        # self.orientation = 0
        # self.horizontalSlider.valueChanged['int'].connect(lambda state: self.update_plot(state))
        # self.horizontalSlider_2.valueChanged['int'].connect(lambda state: self.update_plot(state,1))
        # self.dial.valueChanged['int'].connect(lambda state: self.update_plot(state,2))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        return self.slider_windows, self.slider_isolation, self.dial_orientation, self.previous_button, self.next_button, \
               self.prompt_text, self.isolation_print, self.windows_print, self.orientation_print, self.image

    # def heat_loss_wall(self, T_out, T_in, A_wall, e_wall, Th_cond_wall):
    #     U_wall = Th_cond_wall / e_wall
    #     Q_loss = U_wall * A_wall * (T_out - T_in)
    #     return Q_loss

    # # Computing total energy loss [J] from heat loss information
    # def energy_loss_wall(self, Q, timestep):
    #     E_loss = 0
    #     for i in range(0, len(Q) - 1):
    #         E_loss = E_loss + (Q[i] + Q[i + 1]) / 2 * timestep
    #     return E_loss

    # def update_plot(self, e_wall):
    #     # Reading csv temperature data
    #     e_wall /= 100
    #     e_wall += 0.01
    #     T_file = open('geneva_temperature_2weeks.csv')
    #     T_csvreader = csv.reader(T_file)
    #     next(T_csvreader)
    #     T_out = []
    #     for row in T_csvreader:
    #         T_out.append(row)
    #     T_out = np.reshape(np.array(T_out, dtype=np.float32), len(T_out))

    #     # Constants
    #     T_in = 20  # K, inside desired temperature (assumed constant)
    #     A_wall = 40  # m^2, Wall surface area in contact with outside
    #     timestep = 3600 * 24  # 1-hour timestep between temperature data points
    #     J2kwh = 2.77778 * 10 ** (-7)  # Conversion coefficient between J and kWh
    #     Th_cond_wall = 2.25  # W/m/K, concrecte wall themrla Conductivity

    #     # Running the simulation
    #     Q_loss = self.heat_loss_wall(T_out, T_in, A_wall, e_wall, Th_cond_wall)
    #     E_loss = np.zeros(14)

    #     for i in range(len(Q_loss) - 1):
    #         E_loss[i] = (self.energy_loss_wall(Q_loss[i:i + 2], timestep))
    #     E_loss = E_loss * J2kwh

    #     self.canvas.ydata = E_loss
    #     self.canvas.axes.cla()
    #     self.canvas.axes.plot(self.canvas.xdata, self.canvas.ydata)
    #     self.canvas.axes.set_ybound(-1000, 0)
    #     self.canvas.draw()

    # def update_plot(self,c,who):
    #    if who == 0:
    #        self.window = c
    #    if who == 1:
    #        self.isolation = c
    #    if who == 2:
    #        self.orientation = c

    #    self.canvas.ydata = (self.isolation*(self.canvas.xdata**2) + self.window) + np.exp(self.orientation/180)
    #    self.canvas.axes.cla()  # Clear the canvas.
    #    self.canvas.axes.plot(self.canvas.xdata, self.canvas.ydata, 'r')
    #    self.canvas.axes.set_ybound(-40, 40)
    # Trigger the canvas to update and redraw.
    #    self.canvas.draw()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_parameters.setText(_translate("Form", "PARAMÈTRES"))
        self.label_isolation.setText(_translate("Form", "Épaisseur d'isolation"))
        self.label_windows.setText(_translate("Form", "Surface vitrée"))
        self.label_orientation.setText(_translate("Form", "Orientation"))
        self.label_north.setText(_translate("Form", "N"))
        self.label_south.setText(_translate("Form", "S"))
        self.label_west.setText(_translate("Form", "O"))
        self.label_east.setText(_translate("Form", "E"))
        self.prompt_text.setText(_translate("Form", self.initial_prompt))
        self.isolation_print.setText(_translate("Form", f"{self.slider_isolation.value()/2} cm"))
        self.windows_print.setText(_translate("Form", f"{self.slider_windows.value()} %"))
        self.orientation_print.setText(_translate("Form", f"{self.dial_orientation.value()} °"))


class Window(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec())

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtCore, QtWidgets

def create_window(window, graph):
        window.setObjectName("main  window")
        window.resize(1000, 600)

        label = _create_label(window, 'Parameters', [10, 10, 91, 31])

        _create_label(window, 'window', [10, 40, 61, 21])
        widow_silder = _slider(window, [10, 60, 160, 21])

        _create_label(window, 'isolation', [10, 100, 81, 21])
        isolation_slider = _slider(window, [10, 120, 160, 21])

        _create_label(window, 'orientation', [10, 160, 101, 21])
        orientation_dial = _dial(window, [50, 183, 71, 81])

        _create_graph(window, [100,0,900,600], graph)

        return widow_silder, isolation_slider, orientation_dial

      

# box = [10, 10, 91, 31], the coordinate of the box
def _create_graph(window, box, graph):
    widget = QtWidgets.QWidget(window)
    widget.setGeometry(*box)
    layout = QtWidgets.QVBoxLayout(widget)
    ## TODO understand how it works ???
    graph.setGeometry(QtCore.QRect(200, 10, 431, 251))
    layout.addWidget(graph)


def _create_label(window, name, box):
    label = QtWidgets.QLabel(window)
    label.setGeometry(QtCore.QRect(*box))
    label.setText(name)
    return label

def _slider(window, box):
    slider = QtWidgets.QSlider(window)
    slider.setGeometry(QtCore.QRect(*box))
    slider.setOrientation(QtCore.Qt.Horizontal)
    return slider

def _dial(window, box):
    dial = QtWidgets.QDial(window)
    dial.setGeometry(QtCore.QRect(*box))
    dial.setMaximum(359)
    dial.setPageStep(10)
    dial.setWrapping(True)
    dial.setNotchesVisible(True)
    return dial
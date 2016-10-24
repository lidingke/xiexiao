from __future__ import division
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import threading
import datetime
import pdb


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor = 'white' )
        self.fig = fig
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class TwoLinePlot(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], 'r')

    def update_figure(self):
        self.axes.plot(self.xlist, self.y1list, 'r', \
                       self.xlist, self.y2list, 'b')
        self.draw()

    def XYaxit(self,x,y1,y2):
        # self.xlist = x
        if x:
            self.xlist,self.unit = self._extractUnit(x)
            self.y1list = y1
            self.y2list = y2
            self.update_figure()

    def savePlotFig(self):
        def savefigThread(self):
            self.fig.savefig("data\\plot.svg", format='svg')  # data\
        threading.Thread(target=savefigThread, daemon=True).start()


    def _extractUnit(self, x):
        if len(x)>0:
            timeStatesec = x[-1] - x[0]
            if timeStatesec > 3600:
                xunit = 'hour'
                resultlst = [r / 3600 for r in x]
            elif timeStatesec > 300:  # 5min
                xunit = 'min'
                resultlst = [r / 60 for r in x]
            else:
                xunit = 'sec'
                resultlst = x
            return  resultlst, xunit
        else:
            return x, ''


    def XYaxitList(self, is_, x, y):
        """
        old interface from log
        """
        self.isPloting = is_
        print('getplot ', is_)
        self.xlist = x
        self.y1list = y
        self.axes.plot(self.xlist, self.y1list, 'r')
        self.draw()
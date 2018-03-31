import sys
 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from qtasync import AsyncTask, coroutine 
from PyQt5.QtCore import QCoreApplication, Qt,QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from core import fmaker
import random
from planmaker import make_plan
import numpy as np
import asyncio
class App(QWidget):
    fmaker_ =0
    def __init__(self):
        super().__init__()
        self.left = 400
        self.top = 400
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 800
        self.height = 600
        self.fmaker_ = fmaker()
        self.plan=[[],[]]
        self.initUI()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
        hbox = QHBoxLayout(self)

        topleft = QSplitter(Qt.Vertical)
        topleft.setFrameShape(QFrame.StyledPanel)
        
        splitbutton = QSplitter(Qt.Horizontal)
        splitbutton.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(topleft)
        topleft.addWidget(splitbutton)
        
        parts= []
        for i in range(3):
            parts.append(QSplitter(Qt.Horizontal))
            parts[i].setFrameShape(QFrame.StyledPanel)
            topleft.addWidget(parts[i])

        hbox.addWidget(splitter1)
        
        self.setLayout(hbox)
        self.setWindowTitle('Синтез непрерывных D-планов для нечетких моделей с тремя подобластями')
        self.m = PlotCanvas(splitter1, width=5, height=4)
        self.m.move(0,0)
        self.radiobutton = []
        
        dic = ["в первом","во втором", "в третьем"]
        for i in range(3):
            grid = QGridLayout()
            group_box = QGroupBox("Модель "+dic[i]+" нечетком множестве")
            group_box.setLayout(grid)
            
            self.radiobutton.append(QRadioButton("Квадратичная"))
            self.radiobutton[i * 2].setChecked(True)
            self.radiobutton[i * 2].type = "quad"
            self.radiobutton[i * 2].toggled.connect(self.on_radio_button_toggled1)

            self.radiobutton.append(QRadioButton("Линейная"))
            self.radiobutton[i * 2 + 1].type = "lin"
            self.radiobutton[i * 2 + 1].toggled.connect(self.on_radio_button_toggled1)
            parts[i].addWidget(group_box)
            grid.addWidget(self.radiobutton[i * 2],1,1)
            grid.addWidget(self.radiobutton[i * 2 + 1],2,1)
        
        
      
        button = QPushButton('Сформировать план')
        button.clicked.connect(self.start_calculations)
        splitbutton.addWidget(button)
        self.show()

    def on_radio_button_toggled1(self):
        radiobutton = self.sender()

        if radiobutton.isChecked():
            self.fmaker_.change_model((self.radiobutton.index(radiobutton)+1)//3, radiobutton.type)
            
    @coroutine
    def start_calculations(self,arg):
        button = self.sender()
        button.setText('Производятся вычисления')
        button.setEnabled(False)
        for rb in self.radiobutton:
            rb.setEnabled(False)
        self.plan  = yield AsyncTask(make_plan,self.fmaker_,button)
        self.m.plot(self.plan)
        file = open('plan.txt','w')
        for i in range(len(self.plan[0])):
            file.write(str(self.plan[0][i]) + '\t' + str(self.plan[1][i]) + '\n')
        file.close()
        button.setText('Сформировать план')
        
        button.setEnabled(True)
        for rb in self.radiobutton:
            rb.setEnabled(True)
        
        
    
 
 
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
 
 
    def plot(self, plan):
        data = [random.random() for i in range(25)]
        self.axes.cla()
        self.axes.scatter( x = plan[0], y = [0 for _ in plan[0]],
                          s = 5e3 * np.array(plan[1]), c = np.random.rand(len(plan[0])),
                          alpha = 0.5,
                          label = 'Веса точек в плане')
        self.axes.scatter( x = [0], y = [0],
                          s = 0,
                          alpha = 0.0,
                          label = '|M| = ' + str(plan[2]))
        plt.ylim(-1,1)
        self.axes.legend()
        for i, num in enumerate(plan[1]):
            self.axes.annotate(round(num,3), (plan[0][i]-0.05,plan[1][i]/40))
        self.axes.set_title('План эксперимента')
        self.axes.grid()
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
  
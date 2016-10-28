# coding=utf-8


import sys
# import
# sys.path.append("..")
import pdb
# Library imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QCoreApplication, QFile

# Local imports
from    view.view        import View
from    presenter   import Presenter


def loadStyleSheet( sheetName):

    with open('UI/QSS/{}.qss'.format(sheetName), 'rb') as f:
        styleSheet = f.readlines()
        # print(read)
        styleSheet = b''.join(styleSheet)
        styleSheet = styleSheet.decode('utf-8')
        # pdb.set_trace()
    # file = QFile(':/UI/QSS/%s.qss' % sheetName.lower())
    # file.open(QFile.ReadOnly)
    #
    # styleSheet = file.readAll()
    # styleSheet = str(styleSheet, encoding='utf8')

    return styleSheet



if __name__ == '__main__':

    # QCoreApplication.setLibraryPaths(['C:\\Users\\lidingke\\Envs\\py34qt5\\Lib\\site-packages\\PyQt5\\plugins'])

    # QCoreApplication.setLibraryPaths(['./plugins'])
    # pdb.set_trace()
    _ver = sys.version_info
    if _ver[0] == 3:
        if _ver[1] == 5:
            QCoreApplication.setLibraryPaths(['./plugins/py35'])
        elif _ver[2] == 4:
            QCoreApplication.setLibraryPaths(['./plugins/py34'])

    app = QApplication(sys.argv)
    pt = QPalette()
    pt.setColor(QPalette.Background , QColor('white'))
    # pt.setColor(QPalette.ButtonText, QColor(34,39,42))
    # pt.setColor(QPalette.Button, QColor(239,246,250))
    # pt.setColor(QPalette.WindowText, QColor(34,39,42))
    # pt.setColor(QPalette.Hghlight, QColor(74,149,184))
    app.setPalette(pt)
    app.setStyleSheet(loadStyleSheet('main'))
    font = app.font()
    font.setPointSize(10)
    font.setFamily('微软雅黑')
    app.setFont(font)
    gui         = View()
    presenter   = Presenter(gui)
    gui.show()

    sys.exit(app.exec_())

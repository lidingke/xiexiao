# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportDialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(430, 179)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 406, 118))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditProducer = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditProducer.setObjectName("lineEditProducer")
        self.gridLayout.addWidget(self.lineEditProducer, 3, 1, 1, 1)
        self.labelFiberNo = QtWidgets.QLabel(self.layoutWidget)
        self.labelFiberNo.setObjectName("labelFiberNo")
        self.gridLayout.addWidget(self.labelFiberNo, 3, 2, 1, 1)
        self.lineEditFiberlength = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditFiberlength.setObjectName("lineEditFiberlength")
        self.gridLayout.addWidget(self.lineEditFiberlength, 2, 3, 1, 1)
        self.labelFiberlength = QtWidgets.QLabel(self.layoutWidget)
        self.labelFiberlength.setObjectName("labelFiberlength")
        self.gridLayout.addWidget(self.labelFiberlength, 2, 2, 1, 1)
        self.labelProducer = QtWidgets.QLabel(self.layoutWidget)
        self.labelProducer.setObjectName("labelProducer")
        self.gridLayout.addWidget(self.labelProducer, 3, 0, 1, 1)
        self.lineEditFiberNo = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditFiberNo.setObjectName("lineEditFiberNo")
        self.gridLayout.addWidget(self.lineEditFiberNo, 3, 3, 1, 1)
        self.labelWorker = QtWidgets.QLabel(self.layoutWidget)
        self.labelWorker.setObjectName("labelWorker")
        self.gridLayout.addWidget(self.labelWorker, 1, 0, 1, 1)
        self.lineEditWorker = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditWorker.setObjectName("lineEditWorker")
        self.gridLayout.addWidget(self.lineEditWorker, 1, 1, 1, 1)
        self.labelHumidity = QtWidgets.QLabel(self.layoutWidget)
        self.labelHumidity.setObjectName("labelHumidity")
        self.gridLayout.addWidget(self.labelHumidity, 1, 2, 1, 1)
        self.lineEditDate = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditDate.setObjectName("lineEditDate")
        self.gridLayout.addWidget(self.lineEditDate, 0, 1, 1, 1)
        self.lineEditTemperature = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditTemperature.setObjectName("lineEditTemperature")
        self.gridLayout.addWidget(self.lineEditTemperature, 0, 3, 1, 1)
        self.lineEditHumidity = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditHumidity.setObjectName("lineEditHumidity")
        self.gridLayout.addWidget(self.lineEditHumidity, 1, 3, 1, 1)
        self.labelFibertype = QtWidgets.QLabel(self.layoutWidget)
        self.labelFibertype.setObjectName("labelFibertype")
        self.gridLayout.addWidget(self.labelFibertype, 2, 0, 1, 1)
        self.lineEditFibertype = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditFibertype.setObjectName("lineEditFibertype")
        self.gridLayout.addWidget(self.lineEditFibertype, 2, 1, 1, 1)
        self.labelTemperature = QtWidgets.QLabel(self.layoutWidget)
        self.labelTemperature.setObjectName("labelTemperature")
        self.gridLayout.addWidget(self.labelTemperature, 0, 2, 1, 1)
        self.labelDate = QtWidgets.QLabel(self.layoutWidget)
        self.labelDate.setObjectName("labelDate")
        self.gridLayout.addWidget(self.labelDate, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(220, 140, 150, 23))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.saveButton = QtWidgets.QPushButton(self.splitter)
        self.saveButton.setObjectName("saveButton")
        self.cancelButton = QtWidgets.QPushButton(self.splitter)
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelFiberNo.setText(_translate("Dialog", "光纤编号："))
        self.labelFiberlength.setText(_translate("Dialog", "光纤长度："))
        self.labelProducer.setText(_translate("Dialog", "生产厂家："))
        self.labelWorker.setText(_translate("Dialog", "操作人："))
        self.labelHumidity.setText(_translate("Dialog", "环境湿度："))
        self.labelFibertype.setText(_translate("Dialog", "光纤型号："))
        self.labelTemperature.setText(_translate("Dialog", "环境温度："))
        self.labelDate.setText(_translate("Dialog", "日期："))
        self.saveButton.setText(_translate("Dialog", "保存"))
        self.cancelButton.setText(_translate("Dialog", "取消"))

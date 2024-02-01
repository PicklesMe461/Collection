# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'servo.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
import requests


class Ui_Form(object):

    def __init__(self) -> None:
        self.target_address = "http://192.168.1.103/"


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(646, 262)
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setEnabled(True)
        self.radioButton.setGeometry(QtCore.QRect(70, 80, 112, 23))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.toggled.connect(self.radiobtn_values)
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setEnabled(True)
        self.radioButton_2.setGeometry(QtCore.QRect(120, 80, 112, 23))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.toggled.connect(self.radiobtn_values)
        self.radioButton_3 = QtWidgets.QRadioButton(Form)
        self.radioButton_3.setEnabled(True)
        self.radioButton_3.setGeometry(QtCore.QRect(180, 80, 112, 23))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.toggled.connect(self.radiobtn_values)
        self.radioButton_4 = QtWidgets.QRadioButton(Form)
        self.radioButton_4.setEnabled(True)
        self.radioButton_4.setGeometry(QtCore.QRect(240, 80, 112, 23))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_4.toggled.connect(self.radiobtn_values)
        self.radioButton_5 = QtWidgets.QRadioButton(Form)
        self.radioButton_5.setEnabled(True)
        self.radioButton_5.setGeometry(QtCore.QRect(300, 80, 112, 23))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_5.toggled.connect(self.radiobtn_values)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(380, 70, 181, 41))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton.clicked.connect(self.release_pressed)
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setEnabled(True)
        self.horizontalSlider.setGeometry(QtCore.QRect(80, 160, 481, 20))
        self.horizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.horizontalSlider.setMouseTracking(False)
        self.horizontalSlider.setTabletTracking(False)
        self.horizontalSlider.setAutoFillBackground(False)
        self.horizontalSlider.setMaximum(180)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setProperty("Angle", 0)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(self.slider)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def radiobtn_values(self):    

        if self.radioButton.isChecked():
            self.dutyVal = int(self.radioButton.text())
        elif self.radioButton_2.isChecked(): 
            self.dutyVal = int(self.radioButton_2.text())
        elif self.radioButton_3.isChecked(): 
            self.dutyVal = int(self.radioButton_3.text())
        elif self.radioButton_4.isChecked(): 
            self.dutyVal = int(self.radioButton_4.text())
        elif self.radioButton_5.isChecked(): 
            self.dutyVal = int(self.radioButton_5.text())
        
        print(self.dutyVal)
        try:
            requests.post(self.target_address, data={"PWM" : str(self.dutyVal)})
        except Exception as e:
            print(e)

    
    def release_pressed(self):
        if self.pushButton.isChecked():
            print("Release Motor")
            try:
                requests.post(self.target_address, data={"RELEASE" : 1})
            except Exception as e:
                print(e)
            return "release"

    def slider(self):
        print(self.horizontalSlider.value())
        try:
            requests.post(self.target_address, data={"PWM" : str(self.horizontalSlider.value())})
        except Exception as e:
            print(e)
        return self.horizontalSlider.value()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.radioButton.setText(_translate("Form", "0"))
        self.radioButton_2.setText(_translate("Form", "45"))
        self.radioButton_3.setText(_translate("Form", "90"))
        self.radioButton_4.setText(_translate("Form", "135"))
        self.radioButton_5.setText(_translate("Form", "180"))
        self.pushButton.setText(_translate("Form", "Release Motor"))
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


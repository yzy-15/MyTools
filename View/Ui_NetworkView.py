# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\16639\Documents\WorkSpace\MyTools\View\NetworkView.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NetworkView(object):
    def setupUi(self, NetworkView):
        NetworkView.setObjectName("NetworkView")
        NetworkView.resize(696, 564)
        self.gridLayout = QtWidgets.QGridLayout(NetworkView)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(NetworkView)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(NetworkView)
        QtCore.QMetaObject.connectSlotsByName(NetworkView)

    def retranslateUi(self, NetworkView):
        _translate = QtCore.QCoreApplication.translate
        NetworkView.setWindowTitle(_translate("NetworkView", "Form"))
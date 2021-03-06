# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\16639\Documents\WorkSpace\MyTools\View\CodeAnalysisView.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CodeAnalysisView(object):
    def setupUi(self, CodeAnalysisView):
        CodeAnalysisView.setObjectName("CodeAnalysisView")
        CodeAnalysisView.resize(1022, 581)
        self.gridLayout_2 = QtWidgets.QGridLayout(CodeAnalysisView)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableView = QtWidgets.QTableView(CodeAnalysisView)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(CodeAnalysisView)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(CodeAnalysisView)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 4, 1, 1)
        self.label_9 = QtWidgets.QLabel(CodeAnalysisView)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 4, 1, 1)
        self.commentCount_lineEdit = QtWidgets.QLineEdit(CodeAnalysisView)
        self.commentCount_lineEdit.setReadOnly(True)
        self.commentCount_lineEdit.setObjectName("commentCount_lineEdit")
        self.gridLayout.addWidget(self.commentCount_lineEdit, 2, 3, 1, 1)
        self.byteCount_lineEdit = QtWidgets.QLineEdit(CodeAnalysisView)
        self.byteCount_lineEdit.setReadOnly(True)
        self.byteCount_lineEdit.setObjectName("byteCount_lineEdit")
        self.gridLayout.addWidget(self.byteCount_lineEdit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(CodeAnalysisView)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.filesCount_lineEdit = QtWidgets.QLineEdit(CodeAnalysisView)
        self.filesCount_lineEdit.setReadOnly(True)
        self.filesCount_lineEdit.setObjectName("filesCount_lineEdit")
        self.gridLayout.addWidget(self.filesCount_lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(CodeAnalysisView)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.linesCount_lineEdit = QtWidgets.QLineEdit(CodeAnalysisView)
        self.linesCount_lineEdit.setReadOnly(True)
        self.linesCount_lineEdit.setObjectName("linesCount_lineEdit")
        self.gridLayout.addWidget(self.linesCount_lineEdit, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(CodeAnalysisView)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.projectPath_lineEdit = QtWidgets.QLineEdit(CodeAnalysisView)
        self.projectPath_lineEdit.setReadOnly(True)
        self.projectPath_lineEdit.setObjectName("projectPath_lineEdit")
        self.gridLayout.addWidget(self.projectPath_lineEdit, 0, 5, 1, 1)
        self.codeCount_lineEdit = QtWidgets.QLineEdit(CodeAnalysisView)
        self.codeCount_lineEdit.setReadOnly(True)
        self.codeCount_lineEdit.setObjectName("codeCount_lineEdit")
        self.gridLayout.addWidget(self.codeCount_lineEdit, 0, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(CodeAnalysisView)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(CodeAnalysisView)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.blankCount_lineEdit = QtWidgets.QLineEdit(CodeAnalysisView)
        self.blankCount_lineEdit.setReadOnly(True)
        self.blankCount_lineEdit.setObjectName("blankCount_lineEdit")
        self.gridLayout.addWidget(self.blankCount_lineEdit, 1, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(CodeAnalysisView)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.selectProject_pushButton = QtWidgets.QPushButton(CodeAnalysisView)
        self.selectProject_pushButton.setObjectName("selectProject_pushButton")
        self.gridLayout.addWidget(self.selectProject_pushButton, 0, 6, 1, 1)
        self.selectFiles_pushButton = QtWidgets.QPushButton(CodeAnalysisView)
        self.selectFiles_pushButton.setObjectName("selectFiles_pushButton")
        self.gridLayout.addWidget(self.selectFiles_pushButton, 1, 6, 1, 1)
        self.filePath_lineEdit = QtWidgets.QLineEdit(CodeAnalysisView)
        self.filePath_lineEdit.setReadOnly(True)
        self.filePath_lineEdit.setObjectName("filePath_lineEdit")
        self.gridLayout.addWidget(self.filePath_lineEdit, 1, 5, 1, 1)
        self.clear_pushButton = QtWidgets.QPushButton(CodeAnalysisView)
        self.clear_pushButton.setObjectName("clear_pushButton")
        self.gridLayout.addWidget(self.clear_pushButton, 2, 6, 1, 1)
        self.rules_comboBox = QtWidgets.QComboBox(CodeAnalysisView)
        self.rules_comboBox.setObjectName("rules_comboBox")
        self.gridLayout.addWidget(self.rules_comboBox, 2, 5, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(CodeAnalysisView)
        QtCore.QMetaObject.connectSlotsByName(CodeAnalysisView)
        CodeAnalysisView.setTabOrder(self.filesCount_lineEdit, self.byteCount_lineEdit)
        CodeAnalysisView.setTabOrder(self.byteCount_lineEdit, self.linesCount_lineEdit)
        CodeAnalysisView.setTabOrder(self.linesCount_lineEdit, self.codeCount_lineEdit)
        CodeAnalysisView.setTabOrder(self.codeCount_lineEdit, self.blankCount_lineEdit)
        CodeAnalysisView.setTabOrder(self.blankCount_lineEdit, self.commentCount_lineEdit)
        CodeAnalysisView.setTabOrder(self.commentCount_lineEdit, self.projectPath_lineEdit)
        CodeAnalysisView.setTabOrder(self.projectPath_lineEdit, self.filePath_lineEdit)
        CodeAnalysisView.setTabOrder(self.filePath_lineEdit, self.rules_comboBox)
        CodeAnalysisView.setTabOrder(self.rules_comboBox, self.selectProject_pushButton)
        CodeAnalysisView.setTabOrder(self.selectProject_pushButton, self.selectFiles_pushButton)
        CodeAnalysisView.setTabOrder(self.selectFiles_pushButton, self.clear_pushButton)
        CodeAnalysisView.setTabOrder(self.clear_pushButton, self.tableView)

    def retranslateUi(self, CodeAnalysisView):
        _translate = QtCore.QCoreApplication.translate
        CodeAnalysisView.setWindowTitle(_translate("CodeAnalysisView", "Form"))
        self.label_6.setText(_translate("CodeAnalysisView", "???????????????"))
        self.label_8.setText(_translate("CodeAnalysisView", "???????????????"))
        self.label_9.setText(_translate("CodeAnalysisView", "???????????????"))
        self.label.setText(_translate("CodeAnalysisView", "???????????????"))
        self.label_2.setText(_translate("CodeAnalysisView", "???????????????"))
        self.label_3.setText(_translate("CodeAnalysisView", "????????????"))
        self.label_7.setText(_translate("CodeAnalysisView", "???????????????"))
        self.label_4.setText(_translate("CodeAnalysisView", "???????????????"))
        self.label_5.setText(_translate("CodeAnalysisView", "???????????????"))
        self.selectProject_pushButton.setText(_translate("CodeAnalysisView", "??????????????????"))
        self.selectFiles_pushButton.setText(_translate("CodeAnalysisView", "????????????"))
        self.clear_pushButton.setText(_translate("CodeAnalysisView", "??????"))

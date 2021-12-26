# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtGui import QIcon
from View.Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# from Log.Logger import MyLogger
from Tools.CodeAnalysisTool import CodeAnalysisTool
from Tools.WebDictionary import WebDictionary
from Tools.NetworkTools import NetworkTools

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('./icon/工具箱.png'))
        self.ui.tabWidget.addTab(CodeAnalysisTool(self), QIcon('./icon/统计表.png'), '代码统计工具')
        self.ui.tabWidget.addTab(WebDictionary(self), QIcon('./icon/语言翻译.png'), '在线翻译')
        self.ui.tabWidget.addTab(NetworkTools(self), QIcon('./icon/网络-net.png'), '网络测试工具')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
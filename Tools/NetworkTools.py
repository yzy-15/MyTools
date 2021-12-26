from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from Log.Logger import MyLogger
from View.Ui_NetworkView import Ui_NetworkView
from Tools.TcpServer import TcpServer
from Tools.TcpSocket import TcpSocket
from Tools.UdpSocket import UdpSocket
from Tools.MqttClient import MqttClient

class NetworkTools(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__ui = Ui_NetworkView()
        self.__ui.setupUi(self)
        self.__ui.tabWidget.addTab(TcpServer(self), QIcon('./icon/服务器.png'), 'TCP服务器')
        self.__ui.tabWidget.addTab(TcpSocket(self), QIcon('./icon/4-5客户端.png'), 'TCP客户端')
        self.__ui.tabWidget.addTab(UdpSocket(self), QIcon('./icon/广播.png'), 'UDP服务器/客户端')
        self.__ui.tabWidget.addTab(MqttClient(self), QIcon('./icon/onsmqtt 微消息队列 .png'), 'MQTT客户端')
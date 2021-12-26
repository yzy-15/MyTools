import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress, QAbstractSocket
from View.Ui_TcpSocketView import Ui_TcpSocketView


class TcpSocket(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__ui = Ui_TcpSocketView()
        self.__ui.setupUi(self)
        self.__tcpSocket = QTcpSocket(self)
        self.__isConnected = False
        self.__timer = QTimer()

        self.__ui.connectServer_pushButton.clicked.connect(
            self.__connectServerSlot)
        self.__tcpSocket.connected.connect(self.__connectedSlot)
        self.__tcpSocket.disconnected.connect(self.__disconnectedSlot)
        self.__tcpSocket.readyRead.connect(self.__readyReadSlot)
        self.__ui.send_pushButton.clicked.connect(self.__sendMessageSlot)
        self.__timer.timeout.connect(self.__sendMessageSlot)
        self.__ui.regularlySend_checkBox.clicked.connect(
            self.__regularlySendSlot)
        self.__ui.saveRecive_pushButton.clicked.connect(self.__saveReciveSlot)

    def hexBytesToStr(self, hexBytes: QByteArray) -> str:
        message = str(hexBytes.toHex(), encoding='utf-8')
        message = message.upper()
        tempList = re.findall('.{2}', message)
        return ' '.join(tempList)

    def __saveReciveSlot(self):
        text = self.__ui.textBrowser.toPlainText()
        if not text:
            return
        fileName = QFileDialog.getSaveFileName(self,
                                               '保存消息记录',
                                               QStandardPaths.writableLocation(
                                                   QStandardPaths.DocumentsLocation) + '/客户端通信记录.log',
                                               'log (*.log)')[0]
        if fileName:
            with open(fileName, 'w') as fp:
                fp.write(text)

    def __regularlySendSlot(self, isChecked: bool):
        if not self.__isConnected:
            self.__ui.regularlySend_checkBox.setCheckable(False)
            return
        if isChecked:
            if self.__ui.timeInterval_spinBox.value():
                self.__timer.start(self.__ui.timeInterval_spinBox.value())
                if not self.__ui.pauseDisplay_checkBox.isChecked():
                    text = "{colorStart} [{time}][Port:{port}]: {msg} {colorEnd}".format(
                        colorStart='<font color=\"#BB0000\">',
                        time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                        port=self.__ui.serverPort_spinBox.value(),
                        msg='自动发送消息已开启',
                        colorEnd='</font>')
                    self.__ui.textBrowser.append(text)
            else:
                self.__ui.timeInterval_spinBox.setValue(0)
                self.__ui.regularlySend_checkBox.setCheckable(False)
        else:
            self.__timer.stop()
            if self.__ui.timeInterval_spinBox.value():
                if not self.__ui.pauseDisplay_checkBox.isChecked():
                    text = "{colorStart} [{time}][Port:{port}]: {msg} {colorEnd}".format(
                        colorStart='<font color=\"#BB0000\">',
                        time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                        port=self.__ui.serverPort_spinBox.value(),
                        msg='自动发送消息已关闭',
                        colorEnd='</font>')
                    self.__ui.textBrowser.append(text)

    def __sendMessageSlot(self):
        if not self.__isConnected:
            return
        sendMsg = self.__ui.plainTextEdit.toPlainText()
        showMsg = sendMsg
        if not sendMsg:
            return
        if self.__ui.hexSend_checkBox.isChecked():
            sendMsg = QByteArray.fromHex(sendMsg.encode(encoding='utf-8'))
            tempList = re.findall('.{2}', showMsg)
            showMsg = ' '.join(tempList)
            showMsg = '[HEX]: ' + showMsg
        else:
            sendMsg = QByteArray(sendMsg.encode(encoding='utf-8'))
        self.__tcpSocket.write(sendMsg)

        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}][{clientIP}:{clientPort}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#00BB00\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                clientIP=self.__tcpSocket.peerAddress().toString(),
                clientPort=self.__tcpSocket.peerPort(),
                msg=showMsg,
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)

    def __readyReadSlot(self):
        message = self.__tcpSocket.readAll()
        if self.__ui.hexRecive_checkBox.isChecked():
            message = '[HEX]: ' + self.hexBytesToStr(message)
        else:
            try:
                message = str(message, encoding='utf-8')
            except:
                message = str(message)

        text = "{colorStart} [{time}][{clientIP}:{clientPort}]: {msg} {colorEnd}".format(
            colorStart='<font color=\"#BB0000\">',
            time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
            clientIP=self.__ui.serverIp_lineEdit.text(),
            clientPort=self.__ui.serverPort_spinBox.value(),
            msg=message,
            colorEnd='</font>')
        if not self.__ui.pauseDisplay_checkBox.isChecked():
            self.__ui.textBrowser.append(text)

    def __disconnectedSlot(self):
        self.__isConnected = False
        self.__ui.serverPort_spinBox.setEnabled(True)
        self.__ui.serverIp_lineEdit.setEnabled(True)
        self.__ui.connectServer_pushButton.setText('连接')
        text = "{colorStart} [{time}][{clientIP}:{clientPort}]: {msg} {colorEnd}".format(
            colorStart='<font color=\"#BB0000\">',
            time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
            clientIP=self.__ui.serverIp_lineEdit.text(),
            clientPort=self.__ui.serverPort_spinBox.value(),
            msg='断开连接',
            colorEnd='</font>')
        if not self.__ui.pauseDisplay_checkBox.isChecked():
            self.__ui.textBrowser.append(text)

    def __connectedSlot(self):
        self.__isConnected = True
        self.__ui.serverPort_spinBox.setEnabled(False)
        self.__ui.serverIp_lineEdit.setEnabled(False)
        self.__ui.connectServer_pushButton.setText('断开连接')
        text = "{colorStart} [{time}][{clientIP}:{clientPort}]: {msg} {colorEnd}".format(
            colorStart='<font color=\"#BB0000\">',
            time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
            clientIP=self.__ui.serverIp_lineEdit.text(),
            clientPort=self.__ui.serverPort_spinBox.value(),
            msg='连接成功',
            colorEnd='</font>')
        if not self.__ui.pauseDisplay_checkBox.isChecked():
            self.__ui.textBrowser.append(text)

    def __connectServerSlot(self):
        serverIp = self.__ui.serverIp_lineEdit.text()
        serverPort = self.__ui.serverPort_spinBox.value()
        if self.__isConnected:
            self.__tcpSocket.close()
        else:
            if serverIp and serverPort:
                self.__tcpSocket.connectToHost(serverIp, serverPort)

import re
from typing import List
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress, QAbstractSocket
from View.Ui_TcpServerView import Ui_TcpServerView


class TcpServer(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__ui = Ui_TcpServerView()
        self.__ui.setupUi(self)
        self.__isOpen = False
        self.__timer = QTimer()
        self.__clientListModel = QStandardItemModel(
            self.__ui.connectedClient_tableView)
        self.__clientList = []

        self.__ui.connectedClient_tableView.setModel(self.__clientListModel)
        self.__clientListModel.setHorizontalHeaderLabels(['IP', 'Port'])
        self.__ui.connectedClient_tableView.resizeColumnsToContents()
        self.__ui.connectedClient_tableView.selectedIndexes()
        self.__tcpServer = QTcpServer(self)
        self.__tcpServer.newConnection.connect(self.__newConnectionSlot)
        self.__tcpServer.acceptError.connect(self.__acceptErrorSlot)
        self.__ui.start_pushButton.clicked.connect(
            self.__openOrCloseServerSlot)
        self.__ui.send_pushButton.clicked.connect(self.__sendMessageSlot)
        self.__ui.regularlySend_checkBox.clicked.connect(
            self.__regularlySendSlot)
        self.__timer.timeout.connect(self.__sendMessageSlot)
        self.__ui.saveRecive_pushButton.clicked.connect(self.__saveReciveSlot)

    def hexBytesToStr(self, hexBytes: QByteArray) -> str:
        message = str(hexBytes.toHex(), encoding='utf-8')
        message = message.upper()
        tempList = re.findall('.{2}', message)
        return ' '.join(tempList)

    def openServer(self):
        if self.__isOpen:
            return
        if self.__tcpServer.listen(QHostAddress.Any, self.__ui.serverPort_spinBox.value()):
            self.__ui.start_pushButton.setText('关闭')
            self.__isOpen = True
            self.__ui.serverPort_spinBox.setEnabled(False)
            if not self.__ui.pauseDisplay_checkBox.isChecked():
                text = "{colorStart} [{time}][Port:{port}]: {msg} {colorEnd}".format(
                    colorStart='<font color=\"#BB0000\">',
                    time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                    port=self.__ui.serverPort_spinBox.value(),
                    msg='服务器已开启',
                    colorEnd='</font>')
                self.__ui.textBrowser.append(text)

    def closeServer(self):
        if not self.__isOpen:
            return
        self.__tcpServer.close()
        self.__ui.start_pushButton.setText('开启')
        self.__isOpen = False
        self.__ui.serverPort_spinBox.setEnabled(True)

        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}][Port:{port}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                port=self.__ui.serverPort_spinBox.value(),
                msg='服务器已关闭',
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)
        self.__clientList.clear()
        self.__clientListModel.removeRows(0, self.__clientListModel.rowCount())

    def __saveReciveSlot(self):
        text = self.__ui.textBrowser.toPlainText()
        if not text:
            return
        fileName = QFileDialog.getSaveFileName(self,
                                               '保存消息记录',
                                               QStandardPaths.writableLocation(
                                                   QStandardPaths.DocumentsLocation) + '/服务器通讯.log',
                                               'log (*.log)')[0]
        if fileName: 
            with open(fileName, 'w') as fp:
                fp.write(text)

    def __regularlySendSlot(self, isChecked: bool):
        if not self.__isOpen:
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
        if not self.__isOpen:
            return
        sendMsg = self.__ui.plainTextEdit.toPlainText()
        showMsg = sendMsg
        if not sendMsg:
            return
        if not self.__clientList:
            return
        if self.__ui.hexSend_checkBox.isChecked():
            sendMsg = QByteArray.fromHex(sendMsg.encode(encoding='utf-8'))
            tempList = re.findall('.{2}', showMsg)
            showMsg = ' '.join(tempList)
            showMsg = '[HEX]: ' + showMsg
        else:
            sendMsg = QByteArray(sendMsg.encode(encoding='utf-8'))

        if self.__ui.selectedAll_checkBox.isChecked():
            for client in self.__clientList:
                client.write(sendMsg)

                if not self.__ui.pauseDisplay_checkBox.isChecked():
                    text = "{colorStart} [{time}]发送[{clientIP}:{clientPort}]: {msg} {colorEnd}".format(
                        colorStart='<font color=\"#00BB00\">',
                        time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                        clientIP=client.peerAddress().toString().removeprefix('::ffff:'),
                        clientPort=client.peerPort(),
                        msg=showMsg,
                        colorEnd='</font>')
                    self.__ui.textBrowser.append(text)
        else:
            index = self.__ui.connectedClient_tableView.currentIndex().row()
            if -1 == index:
                return
            client = self.__clientList[index]
            client.write(sendMsg)
            if not self.__ui.pauseDisplay_checkBox.isChecked():
                text = "{colorStart} [{time}]发送[{clientIP}:{clientPort}]: {msg} {colorEnd}".format(
                    colorStart='<font color=\"#00BB00\">',
                    time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                    clientIP=client.peerAddress().toString().removeprefix('::ffff:'),
                    clientPort=client.peerPort(),
                    msg=showMsg,
                    colorEnd='</font>')
                self.__ui.textBrowser.append(text)

    def __openOrCloseServerSlot(self):
        if self.__isOpen:
            self.closeServer()
        else:
            self.openServer()

    def __acceptErrorSlot(self, socketError):
        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}]: SocketError: {msg} {colorEnd}".format(
                colorStart='<font color=\"#FF0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                msg=socketError,
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)
        self.closeServer()

    def __newConnectionSlot(self):
        client = self.__tcpServer.nextPendingConnection()
        self.__clientList.append(client)

        ipStr = client.peerAddress().toString().removeprefix('::ffff:')
        port = client.peerPort()

        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}][{clientIP}:{clientPort}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                clientIP=ipStr,
                clientPort=port,
                msg='新连接',
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)
        self.__clientListModel.appendRow(
            [QStandardItem(ipStr), QStandardItem(str(port))])
        self.__ui.connectedClient_tableView.resizeColumnsToContents()

        client.disconnected.connect(self.__clientDisconnectedSlot)
        client.readyRead.connect(self.__clientReadyReadSlot)

    def __clientReadyReadSlot(self):
        client = self.sender()
        ipStr = client.peerAddress().toString().removeprefix('::ffff:')
        port = client.peerPort()

        if not self.__ui.pauseDisplay_checkBox.isChecked():
            message = client.readAll()
            if self.__ui.hexRecive_checkBox.isChecked():
                message = '[HEX]: ' + self.hexBytesToStr(message)
            else:
                try:
                    message = str(message, encoding='utf-8')
                except:
                    message = str(message)
            text = "{colorStart} [{time}]接收[{clientIP}:{clientPort}]: {msg}{colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                clientIP=ipStr,
                clientPort=port,
                msg=message,
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)

    def __clientDisconnectedSlot(self):
        if not self.__isOpen:
            return
        client = self.sender()
        ipStr = client.peerAddress().toString().removeprefix('::ffff:')
        port = client.peerPort()

        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}][{clientIP}:{clientPort}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                clientIP=ipStr,
                clientPort=port,
                msg='客户端断开连接',
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)
        self.__clientListModel.removeRow(self.__clientList.index(client))
        self.__clientList.remove(client)

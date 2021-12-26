import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QHostAddress, QUdpSocket
from View.Ui_UdpSocketView import Ui_UdpSocketView


class UdpSocket(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__ui = Ui_UdpSocketView()
        self.__ui.setupUi(self)
        self.__udpSocket = QUdpSocket(self)
        self.__isBinded = False
        self.__timer = QTimer()
        # BUG: 测试发现如果没有绑定先向自己发送一个单播后会导致无法绑定端口
        # 目前解决方案是启动时先手动绑定一次
        self.__bindPortSlot()
        self.__ui.textBrowser.clear()

        self.__udpSocket.readyRead.connect(self.__readyReadSlot)
        self.__ui.saveRecive_pushButton.clicked.connect(self.__saveReciveSlot)
        self.__ui.send_pushButton.clicked.connect(self.__sendMsgSlot)
        self.__timer.timeout.connect(self.__sendMsgSlot)
        self.__ui.bindPort_pushButton.clicked.connect(self.__bindPortSlot)
        self.__ui.regularlySend_checkBox.clicked.connect(
            self.__regularlySendSlot)

    def hexBytesToStr(self, hexBytes: QByteArray) -> str:
        message = str(hexBytes.toHex(), encoding='utf-8')
        message = message.upper()
        tempList = re.findall('.{2}', message)
        return ' '.join(tempList)

    def __regularlySendSlot(self, isChecked: bool):
        if isChecked:
            if self.__ui.timeInterval_spinBox.value():
                self.__timer.start(self.__ui.timeInterval_spinBox.value())
                if not self.__ui.pauseDisplay_checkBox.isChecked():
                    text = "{colorStart} [{time}]: {msg} {colorEnd}".format(
                        colorStart='<font color=\"#BB0000\">',
                        time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
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
                    text = "{colorStart} [{time}]: {msg} {colorEnd}".format(
                        colorStart='<font color=\"#BB0000\">',
                        time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                        msg='自动发送消息已关闭',
                        colorEnd='</font>')
                    self.__ui.textBrowser.append(text)

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

    def __bindPortSlot(self):
        if self.__isBinded:
            self.__udpSocket.close()
            self.__ui.bindPort_pushButton.setText('开启')
            self.__isBinded = False

            text = "{colorStart} [{time}][Port:{LOCAL_PORT}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                LOCAL_PORT=self.__ui.bindPort_spinBox.value(),
                msg='取消监听',
                colorEnd='</font>')
            if not self.__ui.pauseDisplay_checkBox.isChecked():
                self.__ui.textBrowser.append(text)

        else:
            bindPort = self.__ui.bindPort_spinBox.value()
            if self.__udpSocket.bind(bindPort, QUdpSocket.ShareAddress):
                self.__ui.bindPort_spinBox.setValue(bindPort)
                self.__ui.bindPort_pushButton.setText('关闭')
                self.__isBinded = True

                text = "{colorStart} [{time}][Port:{LOCAL_PORT}]: {msg} {colorEnd}".format(
                    colorStart='<font color=\"#BB0000\">',
                    time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                    LOCAL_PORT=bindPort,
                    msg='监听端口',
                    colorEnd='</font>')
                if not self.__ui.pauseDisplay_checkBox.isChecked():
                    self.__ui.textBrowser.append(text)

    def __readyReadSlot(self):
        while self.__udpSocket.hasPendingDatagrams():
            message, hostIP, hostPort = self.__udpSocket.readDatagram(
                self.__udpSocket.pendingDatagramSize())
            if self.__ui.hexRecive_checkBox.isChecked():
                message = '[HEX]: ' + self.hexBytesToStr(QByteArray(message))
            else:
                try:
                    message = str(message, encoding='utf-8')
                except:
                    message = str(message)
            text = "{colorStart} [{time}]接收[{HOST_IP}:{HOST_PORT}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                HOST_IP=hostIP.toString().removeprefix('::ffff:'),
                HOST_PORT=hostPort,
                msg=message,
                colorEnd='</font>')
            if not self.__ui.pauseDisplay_checkBox.isChecked():
                self.__ui.textBrowser.append(text)

    def __sendMsgSlot(self):
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

        hostPort = self.__ui.hostPort_spinBox.value()
        hostIp = self.__ui.hostIp_lineEdit.text()
        if hostIp:
            hostIp = QHostAddress(hostIp)
        else:
            hostIp = QHostAddress(QHostAddress.Broadcast)
        self.__udpSocket.writeDatagram(sendMsg, hostIp, hostPort)
        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}]发送[{HOST_IP}:{HOST_PORT}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#00BB00\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                HOST_IP=hostIp.toString(),
                HOST_PORT=hostPort,
                msg=showMsg,
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)

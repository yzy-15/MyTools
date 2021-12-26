import re
from paho.mqtt import client as mqtt
from paho.mqtt.client import MQTTMessage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from View.Ui_MqttView import Ui_MqttView


class MqttClient(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__ui = Ui_MqttView()
        self.__ui.setupUi(self)
        self.__connack_string = mqtt.connack_string
        self.__isConnected = False
        self.__timer = QTimer()
        self.__subTopicListModel = QStandardItemModel(
            self.__ui.subTopicList_listView)
        self.__ui.subTopicList_listView.setModel(self.__subTopicListModel)

        # clean_session: True，则代理将在断开此客户端时删除有关该客户端的所有信息。
        # clean_session: False，则客户端是持久客户端，当客户端断开连接时，将保留订阅信息和排队消息。
        self.__mqttClient = mqtt.Client(
            client_id='Sean-Yu', clean_session=False)

        self.__ui.saveRecive_pushButton.clicked.connect(self.__saveReciveSlot)
        self.__ui.send_pushButton.clicked.connect(self.__sendMsgSlot)
        self.__timer.timeout.connect(self.__sendMsgSlot)
        self.__ui.connect_pushButton.clicked.connect(self.__connectServerSlot)
        self.__ui.regularlySend_checkBox.clicked.connect(
            self.__regularlySendSlot)
        self.__ui.addTopic_pushButton.clicked.connect(self.__addSubTopicSlot)
        self.__ui.deleteTopic_pushButton.clicked.connect(
            self.__deleteTopicSlot)

        self.__mqttClient.on_connect = self.__connectSlot
        self.__mqttClient.on_disconnect = self.__disconnectSlot
        self.__mqttClient.on_message = self.__reciveMessageSlot

    def __reciveMessageSlot(self, client, userdata, message: MQTTMessage):
        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}]接收[Topic: {Topic} QoS: {Qos}]: {MSG}{colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                Topic=message.topic,
                Qos=message.qos,
                MSG=str(message.payload, encoding='utf-8'),
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)

    def __disconnectSlot(self, client, userdata, rc):
        disconnectMsg = ''
        if 0 == rc:
            self.__ui.connect_pushButton.setText('连接')
            self.__isConnected = False
            disconnectMsg = '断开连接'
        else:
            disconnectMsg = '断开连接失败：{}'.format(self.__connack_string(rc))
        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                msg=disconnectMsg,
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)

    def __connectSlot(self, client, userdata, flags, rc):
        connectMsg = ''
        if 0 == rc:
            self.__ui.connect_pushButton.setText('断开连接')
            self.__isConnected = True
            connectMsg = '连接成功'
        else:
            connectMsg = '连接失败：{}'.format(self.__connack_string(rc))
        if not self.__ui.pauseDisplay_checkBox.isChecked():
            text = "{colorStart} [{time}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#BB0000\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                msg=connectMsg,
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)

    def __deleteTopicSlot(self):
        for index in self.__ui.subTopicList_listView.selectedIndexes():
            topic = self.__subTopicListModel.item(index.row()).text()
            if mqtt.MQTT_ERR_SUCCESS == self.__mqttClient.unsubscribe(topic)[0]:
                text = "{colorStart} [{time}][Topic: {Topic}]: {msg}{colorEnd}".format(
                    colorStart='<font color=\"#00BB00\">',
                    time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                    Topic=topic,
                    msg='取消订阅',
                    colorEnd='</font>')
                self.__ui.textBrowser.append(text)
                self.__subTopicListModel.removeRow(index.row())

    def __addSubTopicSlot(self):
        if not self.__isConnected:
            return
        topic = self.__ui.addTopic_lineEdit.text()
        if not topic:
            return
        if mqtt.MQTT_ERR_SUCCESS == self.__mqttClient.subscribe(topic)[0]:
            if not self.__ui.pauseDisplay_checkBox.isChecked():
                text = "{colorStart} [{time}][Topic: {Topic}]: {msg}{colorEnd}".format(
                    colorStart='<font color=\"#00BB00\">',
                    time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                    Topic=topic,
                    msg='添加订阅',
                    colorEnd='</font>')
                self.__ui.textBrowser.append(text)
            if self.__subTopicListModel.findItems(topic):
                return
            self.__subTopicListModel.appendRow(QStandardItem(topic))

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

    def __sendMsgSlot(self):
        if not self.__isConnected:
            return
        topic = self.__ui.pubTopic_lineEdit.text()
        if not topic:
            return
        sendMsg = self.__ui.plainTextEdit.toPlainText()
        if not sendMsg:
            return
        qos = self.__ui.qos_spinBox.value()
        if mqtt.MQTT_ERR_SUCCESS == self.__mqttClient.publish(topic, sendMsg, qos).rc:
            text = "{colorStart} [{time}]发送[Topic: {Topic} QoS: {Qos}]: {msg} {colorEnd}".format(
                colorStart='<font color=\"#00BB00\">',
                time=QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss.zzz'),
                Topic=topic,
                Qos=qos,
                msg=sendMsg,
                colorEnd='</font>')
            self.__ui.textBrowser.append(text)
        else:
            QMessageBox.warning(self, '警告', '消息发送失败！')

    def __connectServerSlot(self):
        if self.__isConnected:
            self.__mqttClient.disconnect()
            self.__mqttClient.loop_stop()
            self.__ui.connect_pushButton.setText('连接')
            self.__isConnected = False
        else:
            userName = self.__ui.user_lineEdit.text()
            password = self.__ui.password_lineEdit.text()
            if userName and password:
                self.__mqttClient.username_pw_set(userName, password)

            host = self.__ui.host_lineEdit.text()
            if not host:
                QMessageBox.warning(self, '警告', 'MQTT服务器地址不能为空！')
                return
            port = self.__ui.port_spinBox.value()
            if not port:
                port = 1883
                self.__ui.port_spinBox.setValue(port)
            try:
                self.__mqttClient.connect_async(host, port)
                self.__mqttClient.loop_start()
            except:
                QMessageBox.warning('self', '错误', '连接失败')

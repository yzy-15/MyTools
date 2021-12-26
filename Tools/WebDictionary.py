# -*- coding: utf-8 -*-
import json
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from View.Ui_WebDictionaryView import Ui_WebDictionaryView
'''
{
    'i':transtr,
    'from':'AUTO',
    'TO':'AUTO',
    'smartresult': 'dict',
    'client':'fanyideskweb',
    'salt':salt,
    'sign':sign,
    'ts':ts,
    'bv':bv,
    'doctype':'json',
    'version':'2.1',
    'keyfrom':'fanyi.web',
    'action':'FY_BY_REALTlME'
}
'''


class WebDictionary(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__ui = Ui_WebDictionaryView()
        self.__ui.setupUi(self)
        self.__url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
        # self.__url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.__key = {
            'i': '',
            'from': 'AUTO',
            'TO': 'AUTO',
            'smartresult': 'dict',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'ue': 'UTF-8',
            # 'action': 'FY_BY_CLICKBUTTON',
            'action': 'FY_BY_REALTlME',
            'typoResult': 'true'
        }
        self.__ui.pushButton.clicked.connect(self.__TranslateSlot)
        self.__ui.pushButton.setToolTip('Ctrl+Enter')

    def __TranslateSlot(self):
        self.__ui.textBrowser.setPlainText('')
        word = self.__ui.plainTextEdit.toPlainText()
        if not word:
            return
        self.__key['i'] = word
        response = requests.post(self.__url, data=self.__key)
        # 判断服务器是否相应成功
        if 200 == response.status_code:
            resultJson = response.json()
            # print(resultJson['translateResult'][0])
            # print(resultJson['translateResult'][1])
            # resultJson['translateResult']是二维数组，可能多行，也可能多列，
            # 根据'\n'来决定有几行，根据'.'和';'决定有几列
            for resultRow in resultJson['translateResult']:
                # print(resultRow)
                for resultColumn in resultRow:
                    if not self.__ui.textBrowser.toPlainText():
                        self.__ui.textBrowser.setPlainText(
                            resultColumn['tgt'])
                    else:
                        self.__ui.textBrowser.moveCursor(QTextCursor.End)
                        self.__ui.textBrowser.insertPlainText(
                            resultColumn['tgt'])
                self.__ui.textBrowser.append('')
                    
        else:
            print(response.json())
            self.__ui.textBrowser.setPlainText('有道词典调用失败')

'''
aaa = {
    'type': 'ZH_CN2EN', 
    'errorCode': 0, 
    'elapsedTime': 1, 
    'translateResult': 
    [
        [
            {'src': '你好；', 'tgt': 'How do you do;'}, 
            {'src': '世界', 'tgt': 'The world'}
        ]
    ]
}
'''
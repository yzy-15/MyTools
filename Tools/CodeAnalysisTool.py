# -*- coding: utf-8 -*-
import json
from typing import Tuple
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from Log.Logger import MyLogger
from View.Ui_CodeAnalysisView import Ui_CodeAnalysisView


class CodeAnalysisTool(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        # 初始化变量
        self.__fileCount = 0
        self.__projectSize = 0
        self.__lineCount = 0
        self.__codeCount = 0
        self.__blankCount = 0
        self.__commentCount = 0

        self.__ui = Ui_CodeAnalysisView()
        self.__ui.setupUi(self)
        self.__initUI()

    # 初始化界面
    def __initUI(self) -> None:
        self.__model = QStandardItemModel()
        self.__ui.tableView.setModel(self.__model)
        self.__model.setHorizontalHeaderLabels(
            ["文件名称", "文件类型", "文件大小", "总行数", "代码行数", "注释行数", "空白行数", "代码行数占比", "文件路径"])
        self.__ui.selectProject_pushButton.clicked.connect(
            self.__selectProjectPath_slot
        )
        self.__ui.selectFiles_pushButton.clicked.connect(
            self.__selectFiles_slot
        )
        self.__ui.clear_pushButton.clicked.connect(
            self.__clearUI
        )
        # 加载筛选模式
        self.__rulesDict = dict()
        with open('./ini/rules.json', 'r', encoding='UTF-8') as file:
            self.__rulesDict = json.load(file)
        for key in self.__rulesDict.keys():
            if '规则说明' == key:
                continue
            self.__ui.rules_comboBox.addItem(key)

    # 获取文件行数
    def __getFileLines(self,
                       fileName: str,
                       lineCommentRule: list,
                       paragraphComment: list) -> Tuple:
        # print(lineCommentRule)
        # print(paragraphComment)
        file = open(fileName, 'r', encoding='UTF-8')
        isComment = False
        codeCount = 0
        blankCount = 0
        commentCount = 0

        # 临时记录当前的段注释模式
        tempParagraphComment = []
        for line in file.readlines():
            line = line.strip('\n')
            line = line.strip()
            # 检查段注释开头
            for comment in paragraphComment:
                if line.startswith(comment[0]):
                    tempParagraphComment = comment
                    isComment = True
                    # 移除段注释开头，防止注释开头和注释结尾相同时引发的解析异常
                    line = line[len(comment[0]):]
                    continue
            if isComment:
                commentCount += 1
                # 当已经开始段注释时才判断是否存在段注释结尾
                if line.endswith(tempParagraphComment[1]):
                    isComment = False
            else:
                # 检查行注释
                if line.startswith(tuple(lineCommentRule)):
                    # print(line)
                    commentCount += 1
                # 检查空行
                elif '' == line:
                    blankCount += 1
                else:
                    codeCount += 1

        file.close()
        return (codeCount, blankCount, commentCount)

    # 检查项目文件
    def __checkFile(self, filePathName: str):
        fileRules = dict(
            self.__rulesDict[self.__ui.rules_comboBox.currentText()])
        fileTypeList = list(fileRules["Type"])
        ignoreList = list(fileRules["Ignore"])
        fileinfo = QFileInfo(filePathName)
        fileNmae = fileinfo.fileName()
        if fileNmae.startswith('.'):
            return
        if fileNmae in ignoreList:
            return
        fileSize = fileinfo.size()
        filePath = fileinfo.absolutePath()
        countLines = 0
        codeLines = 0
        blankLines = 0
        commentLines = 0

        for fileType in fileTypeList:
            fileType = str(fileType)
            if fileType.endswith(fileinfo.completeSuffix()):
                fileLines = self.__getFileLines(filePathName,
                                                fileRules['LineComment'],
                                                fileRules['ParagraphComment'])
                codeLines = int(fileLines[0])
                blankLines = int(fileLines[1])
                commentLines = int(fileLines[2])
                countLines = codeLines + blankLines + commentLines
                percent = codeLines * 100 / countLines
                percent = round(percent, 2)
                self.__model.appendRow([QStandardItem(fileNmae),
                                        QStandardItem(
                                            fileinfo.completeSuffix()),
                                        QStandardItem(str(fileSize)),
                                        QStandardItem(str(countLines)),
                                        QStandardItem(str(codeLines)),
                                        QStandardItem(str(commentLines)),
                                        QStandardItem(str(blankLines)),
                                        QStandardItem(str(percent) + '%'),
                                        QStandardItem(filePath)])

                self.__fileCount += 1
                self.__projectSize += fileSize
                self.__lineCount += countLines
                self.__codeCount += codeLines
                self.__blankCount += blankLines
                self.__commentCount += commentLines

    # 分析项目文件
    def __countCode(self, filePath: str):
        dir = QDir(filePath)
        # fileInfo = QFileInfo()
        for fileInfo in dir.entryInfoList():
            if fileInfo.isFile():
                self.__checkFile(fileInfo.absoluteFilePath())
            elif fileInfo.isDir():
                if '.' == fileInfo.fileName() or '..' == fileInfo.fileName():
                    continue
                self.__countCode(fileInfo.absoluteFilePath())
    # 显示统计数据

    def __showCount(self):
        percentCode = 0.00
        percenBlank = 0.00
        percentComment = 0.00
        if self.__lineCount:
            percentCode = self.__codeCount * 100 / self.__lineCount
            percenBlank = self.__blankCount * 100 / self.__lineCount
            percentComment = self.__commentCount * 100 / self.__lineCount
        percentCode = round(percentCode, 2)
        percenBlank = round(percenBlank, 2)
        percentComment = round(percentComment, 2)
        self.__ui.filesCount_lineEdit.setText(str(self.__fileCount))
        self.__ui.byteCount_lineEdit.setText(str(self.__projectSize))
        self.__ui.linesCount_lineEdit.setText(str(self.__lineCount))
        self.__ui.codeCount_lineEdit.setText(str(self.__codeCount))
        self.__ui.codeCount_lineEdit.setToolTip(
            '代码行数占比: ' + str(percentCode) + '%')
        self.__ui.blankCount_lineEdit.setText(str(self.__blankCount))
        self.__ui.blankCount_lineEdit.setToolTip(
            '空白行数占比: ' + str(percenBlank) + '%')
        self.__ui.commentCount_lineEdit.setText(str(self.__commentCount))
        self.__ui.commentCount_lineEdit.setToolTip(
            '注释行数占比: ' + str(percentComment) + '%')

    def __clearUI(self):
        self.__model.removeRows(0, self.__model.rowCount())
        self.__ui.tableView.resizeColumnsToContents()
        self.__fileCount = 0
        self.__projectSize = 0
        self.__lineCount = 0
        self.__codeCount = 0
        self.__blankCount = 0
        self.__commentCount = 0
        self.__showCount()
        self.__ui.filePath_lineEdit.setText('')
        self.__ui.projectPath_lineEdit.setText('')

    # 选择项目路径槽函数
    def __selectProjectPath_slot(self):
        projectPath = QFileDialog.getExistingDirectory(self, "选择项目路径",
                                                       QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation))
        if len(projectPath):
            self.__ui.projectPath_lineEdit.setText(projectPath)
            self.__countCode(projectPath)
            self.__ui.tableView.resizeColumnsToContents()
            self.__showCount()

    # 选择文件槽函数

    def __selectFiles_slot(self):
        fileRules = dict(
            self.__rulesDict[self.__ui.rules_comboBox.currentText()])
        fileTypeList = ' '.join(fileRules["Type"])

        fileTypeList = self.__ui.rules_comboBox.currentText() + ' (' + fileTypeList + ')'
        fileList = QFileDialog.getOpenFileNames(self,
                                                "选择项目路径",
                                                QStandardPaths.writableLocation(
                                                    QStandardPaths.DocumentsLocation),
                                                fileTypeList)
        fileList = fileList[0]
        fileNames = ''
        if fileList:
            for file in fileList:
                self.__checkFile(file)
                fileName = file.split('/')[-1]
                if not fileNames:
                    fileNames = fileName
                else:
                    fileNames += ',' + fileName
        self.__ui.filePath_lineEdit.setText(fileNames)
        self.__ui.tableView.resizeColumnsToContents()
        self.__showCount()

# -*- coding: UTF-8 -*-
import logging
import logging.config
import os
from typing import Awaitable
'''
class LoggerModule(logging.Logger):
    def __init__(self, filename=None):
        super(LoggerModule, self).__init__(self)
        # 日志文件名
        if filename is None:
            filename = './logs/pt.log'
        self.__filename = filename

        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.__filename, 'D', 1,
                                                       30)
        fh.suffix = "%Y%m%d-%H%M.log"
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s][%(filename)s Line:%(lineno)d] [PID:%(process)s TID:%(thread)s][%(levelname)s]: %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.addHandler(fh)
        self.addHandler(ch)
    # def DEBUG(self, info:str):
    #     self.debug(info)
    # def INFO(self, info:str):
    #     self.info(info)
    # def WARN(self, info:str):
    #     self.warning(info)
    # def ERROR(self, info:str):
    #     self.error(info)

class LoggerModule:
    def __init__(self) -> None:
        self.__logFileName = ''
        self.__isInit = False
        self.__logger: logging.Logger
    def setLogFileName(self, logFileName: str):
        self.__isInit = True
        self.__logFileName = logFileName
        if not logFileName:
            self.__logFileName = 'MyLogger.log'
        self.__logger = logging.getLogger(self.__logFileName)
        
        fh = logging.handlers.TimedRotatingFileHandler(self.__logFileName, 'D', 1, 30)
        fh.suffix = "%Y%m%d-%H%M.log"
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s][%(filename)s Line:%(lineno)d] [PID:%(process)s TID:%(thread)s][%(levelname)s]: %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.__logger.addHandler(fh)
        self.__logger.addHandler(ch)
    def getLogger(self):
        if self.__isInit:
            return self.__logger
        return None
'''
class InitLogModule:
    def __init__(self, logConf: str) -> None:
        logging.config.fileConfig('./ini/logging.conf')
        self.__logger = logging.getLogger('Sean')
    def getLogger(self):
        return self.__logger

# 单例模式
MyLogger = InitLogModule('./ini/logging.conf').getLogger()


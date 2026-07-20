import os
from collections import namedtuple
from enum import Enum, IntEnum, auto
from typing import List, Final

from lib.lib_version import LIB_APP_NAME

__ScriptMode: Final = True

if __ScriptMode:
    '''以脚本形式调试、运行时使用（此种形式可在任意位置调用框架模块，不用担心资源路径异常）'''
    LIB_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
else:
    '''打包成exe时使用 or 以完整脚本形式运行时使用'''
    LIB_PROJECT_DIR = os.path.abspath(os.getcwd())

''' Roaming 存放程序运行时输出文件路径（临时线损文件、临时文件…）'''
LIB_ROAMING_APPDATA = os.getenv('APPDATA')

''' Local 存放软件配置文件、日志文件、线损文件路径 '''
LIB_LOCAL_APPDATA = os.getenv('LOCALAPPDATA')

LIB_RESOURCE_DIR = os.path.normpath(f"{LIB_PROJECT_DIR}\\resources")
LIB_IMAGE_DIR = os.path.normpath(LIB_RESOURCE_DIR + "\\images")
LIB_CONFIG_DIR = os.path.normpath(f"{LIB_RESOURCE_DIR}\\config")
LIB_FONT_DIR = os.path.normpath(f"{LIB_RESOURCE_DIR}\\fonts")
LIB_VERIFICATION_KITS_DIR = os.path.normpath(f"{LIB_RESOURCE_DIR}\\verification_kits")
LIB_CSS_DIR = os.path.normpath(f"{LIB_RESOURCE_DIR}\\css")

LIB_TEMP_DIR = os.path.normpath(f"{LIB_ROAMING_APPDATA}\\{LIB_APP_NAME}\\tmp")

LIB_LOG_DIR = os.path.normpath(f"{LIB_LOCAL_APPDATA}\\{LIB_APP_NAME}\\log")  # 日志文件保存路径



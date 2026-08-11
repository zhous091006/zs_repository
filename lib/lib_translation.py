import os
import sys

from cfg.cfg_if import cfg_if
from lib.lib_type import LibLanguageType

LIB_TRANS_DATA_DICT: dict = {}
LIB_SYS_LANGUAGE_TYPE: LibLanguageType = LibLanguageType.AUTO


def tr(words: str):
    if LIB_SYS_LANGUAGE_TYPE == LibLanguageType.ENGLISH:
        return words
    file_name = os.path.basename(sys._getframe().f_back.f_code.co_filename)
    if file_name in LIB_TRANS_DATA_DICT and words in LIB_TRANS_DATA_DICT[file_name]:
        return LIB_TRANS_DATA_DICT[file_name][words]
    if "default" in LIB_TRANS_DATA_DICT and words in LIB_TRANS_DATA_DICT["default"]:
        return LIB_TRANS_DATA_DICT["default"][words]
    # print(file_name, " !Translation not found :", words)
    return words


def tr_language_update():
    global LIB_TRANS_DATA_DICT
    global LIB_SYS_LANGUAGE_TYPE
    LIB_TRANS_DATA_DICT = cfg_if.load_config_file("translation_en_zh.yaml")
    LIB_SYS_LANGUAGE_TYPE = cfg_if.get_language_type()

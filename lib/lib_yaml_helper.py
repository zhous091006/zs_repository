import os
import threading
from functools import wraps
from typing import List, Any

import ruamel.yaml
import yaml
from ruamel.yaml.comments import CommentedMap

from lib.lib_debug import lib_debug_t
from lib.lib_func import lib_func_t

__rlock = threading.RLock()


def _lock_wraps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with __rlock:
            return func(*args, **kwargs)

    return wrapper


class LibYamlHelper:

    @staticmethod
    @_lock_wraps
    def load_yaml_file(file_path: str) -> dict:
        """
        加载yaml文件
        """
        datas = {}
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                datas = yaml.load(f.read(), Loader=yaml.FullLoader)
        return datas

    @staticmethod
    @_lock_wraps
    def save_yaml_file(file_path: str, data: dict) -> bool:
        """
        将字典数据保存为yaml文件（不推荐使用，会清除原有注释）
        """
        if lib_func_t.create_dir_path(os.path.dirname(file_path)):
            try:
                with open(file_path, "w", encoding='utf-8') as f:
                    yaml.dump(data, f)
                return True
            except BaseException as e:
                print(e)
        return False

    @staticmethod
    @_lock_wraps
    def read_node_value(file_path: str, node_keys: List[str], default=None, be_quiet=False) -> Any:
        """
        读取yaml文件节点信息
        """
        try:
            data = LibYamlHelper.load_yaml_file(file_path)
            ret = data
            for key in node_keys:
                ret = ret[key]
            return ret
        except BaseException as e:
            if not be_quiet:
                lib_debug_t.print_except(e)
        return default

    @staticmethod
    @_lock_wraps
    def write_node_value(file_path: str, node_keys: List[str], value) -> bool:
        """
        修改yaml文件节点数据值
        """
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                doc: CommentedMap = ruamel.yaml.round_trip_load(f, preserve_quotes=True)
            p: CommentedMap = doc
            for i in range(len(node_keys) - 1):
                p = p[node_keys[i]]
            p[node_keys[-1]] = value
            with open(file_path, 'w', encoding="utf-8") as f:
                ruamel.yaml.round_trip_dump(doc, f, default_flow_style=False)
            return True
        except BaseException as e:
            lib_debug_t.print_except(e)
        return False

    @staticmethod
    @_lock_wraps
    def write_doc_node_value(doc: CommentedMap, node_keys: List[str], value) -> bool:
        """
        修改yaml文件节点数据值
        """
        try:
            p: CommentedMap = doc
            for i in range(len(node_keys) - 1):
                p = p[node_keys[i]]
            p[node_keys[-1]] = value
            return True
        except BaseException as e:
            lib_debug_t.print_except(e)
        return False


lib_yaml_helper_t = LibYamlHelper

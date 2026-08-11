import ctypes
import threading
from functools import wraps
from typing import List, Any

# from cfg.cfg_manager import CfgManager
from lib.lib_type import LIB_CONFIG_DIR, LibLanguageType
from lib.lib_yaml_helper import LibYamlHelper

__rlock = threading.RLock()


def cfg_lock_wraps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with __rlock:
            return func(*args, **kwargs)

    return wrapper


class CfgIf:

    @staticmethod
    def read_config_file(file_path: str) -> Any:
        return LibYamlHelper.load_yaml_file(file_path)

    @staticmethod
    def load_config_file(filename: str) -> dict:
        return LibYamlHelper.load_yaml_file(f"{LIB_CONFIG_DIR}\\{filename}")

    @staticmethod
    def load_user_config_file(filename: str, default=None) -> dict:
        data = LibYamlHelper.load_yaml_file(f"{LIB_CONFIG_DIR}\\user\\{filename}")
        if data is None:
            return default
        return data

    @staticmethod
    def save_user_config_file(filename: str, data: dict):
        """！！！不推荐使用，会清除原有注释"""
        return LibYamlHelper.save_yaml_file(f"{LIB_CONFIG_DIR}\\user\\{filename}", data)

    @staticmethod
    def read_config(filename: str, keys: List[str], default=None, be_quiet=False) -> Any:
        return LibYamlHelper.read_node_value(f"{LIB_CONFIG_DIR}\\{filename}", keys, default, be_quiet)

    @staticmethod
    def write_config(filename: str, keys: List[str], config) -> bool:
        return LibYamlHelper.write_node_value(f"{LIB_CONFIG_DIR}\\{filename}", keys, config)

    @staticmethod
    def read_user_config(filename: str, keys: List[str], default=None, be_quiet=False) -> Any:
        return cfg_if.read_config(f"user\\{filename}", keys, default, be_quiet)

    @staticmethod
    def write_user_config(filename: str, keys: List[str], config):
        cfg_if.write_config(f"user\\{filename}", keys, config)

    @staticmethod
    @cfg_lock_wraps
    def set_language_type(language_type: LibLanguageType = LibLanguageType.AUTO):
        CfgManager.get_inst().global_setting_model.update_settings(language=language_type)

    @staticmethod
    @cfg_lock_wraps
    def get_language_type() -> LibLanguageType:
        language_type = CfgManager.get_inst().global_setting_model.data.language
        if language_type == LibLanguageType.AUTO:
            dll_handle = ctypes.windll.kernel32
            sys_lang = hex(dll_handle.GetSystemDefaultUILanguage())
            return LibLanguageType.CHINESE if sys_lang.endswith("804") else LibLanguageType.ENGLISH
        return language_type

    @staticmethod
    @cfg_lock_wraps
    def get_local_upload_data_root_path():
        data = CfgManager.get_inst().tasks_setting_model.data.local_upload_data_root_path
        return data

    @staticmethod
    @cfg_lock_wraps
    def get_local_upload_success_backup_root_path():
        data = CfgManager.get_inst().tasks_setting_model.data.local_upload_success_backup_root_path
        return data

    @staticmethod
    @cfg_lock_wraps
    def get_calibration_report_folder_name():
        data = CfgManager.get_inst().tasks_setting_model.data.cali_report_folder_name
        return data

    @staticmethod
    @cfg_lock_wraps
    def get_pv_report_folder_name():
        data = CfgManager.get_inst().tasks_setting_model.data.pv_report_folder_name
        return data

    # @staticmethod
    # @cfg_lock_wraps
    # def get_qa_report_folder_name():
    #     data = CfgManager.get_inst().tasks_setting_model.data.qa_report_folder_name
    #     return data

    @staticmethod
    @cfg_lock_wraps
    def get_sn_id_report_folder_name():
        data = CfgManager.get_inst().tasks_setting_model.data.sn_id_report_folder_name
        return data

    @staticmethod
    @cfg_lock_wraps
    def get_pretest_report_folder_name():
        data = CfgManager.get_inst().tasks_setting_model.data.pretest_report_folder_name
        return data

    @staticmethod
    @cfg_lock_wraps
    def get_aging_test_report_folder_name():
        data = CfgManager.get_inst().tasks_setting_model.data.aging_test_report_folder_name
        return data

    @staticmethod
    def get_calibration_report_path():
        return cfg_if.get_local_upload_data_root_path() + "\\" + cfg_if.get_calibration_report_folder_name()

    @staticmethod
    def get_pv_report_path():
        return cfg_if.get_local_upload_data_root_path() + "\\" + cfg_if.get_pv_report_folder_name()

    # @staticmethod
    # def get_qa_report_path():
    #     return cfg_if.get_local_upload_data_root_path() + "\\" + cfg_if.get_qa_report_folder_name()

    @staticmethod
    def get_sn_id_report_path():
        return cfg_if.get_local_upload_data_root_path() + "\\" + cfg_if.get_sn_id_report_folder_name()

    @staticmethod
    def get_pretest_report_path():
        return cfg_if.get_local_upload_data_root_path() + "\\" + cfg_if.get_pretest_report_folder_name()

    @staticmethod
    def get_aging_test_report_path():
        return cfg_if.get_local_upload_data_root_path() + "\\" + cfg_if.get_aging_test_report_folder_name()

    @staticmethod
    @cfg_lock_wraps
    def get_easy_certificate_path():
        return CfgManager.get_inst().tasks_setting_model.data.easy_certificate_path

    ''' --------------------------------------- Account --------------------------------------- '''

    @staticmethod
    @cfg_lock_wraps
    def get_last_account_username() -> str:
        """获取上次登录用户名"""
        return CfgManager.get_inst().account_setting.data.account_username

    @staticmethod
    @cfg_lock_wraps
    def get_last_account_password() -> str:
        """获取上次登录密码"""
        return CfgManager.get_inst().account_setting.get_account_password()

    @staticmethod
    @cfg_lock_wraps
    def is_auto_login_account() -> bool:
        """是否自动登录"""
        return CfgManager.get_inst().account_setting.data.auto_login

    @staticmethod
    @cfg_lock_wraps
    def is_remember_account_password() -> bool:
        """是否记住密码"""
        return CfgManager.get_inst().account_setting.data.remember_password

    @staticmethod
    @cfg_lock_wraps
    def record_account_username(username: str) -> bool:
        """记录账户名称"""
        return CfgManager.get_inst().account_setting.record_account_username(username)

    @staticmethod
    @cfg_lock_wraps
    def record_account_password(password: str) -> bool:
        """记录账户密码"""
        return CfgManager.get_inst().account_setting.record_account_password(password)

    @staticmethod
    @cfg_lock_wraps
    def set_auto_login_account_state(state: bool) -> bool:
        """设置自动登录账户使能"""
        return CfgManager.get_inst().account_setting.set_auto_login_state(state)

    @staticmethod
    @cfg_lock_wraps
    def set_remember_account_password_state(state: bool) -> bool:
        """设置记录账户密码使能"""
        return CfgManager.get_inst().account_setting.set_remember_password_state(state)

    @staticmethod
    @cfg_lock_wraps
    def record_db_config(host: str, port: int, username: str, password: str) -> bool:
        """记录生产数据库配置"""
        return CfgManager.get_inst().account_setting.record_db_config(host, port, username, password)

    @staticmethod
    @cfg_lock_wraps
    def get_db_config() -> (str, int, str, str):
        """获取生产数据库配置"""
        return CfgManager.get_inst().account_setting.get_db_config()

    ''' ------------------------------------------------------------------------------ '''

    @staticmethod
    def set_tmp_config(keys: List[str], value):
        data = cfg_if.load_user_config_file("tmp.yaml", default={})
        data["::".join(keys)] = value
        cfg_if.save_user_config_file("tmp.yaml", data)

    @staticmethod
    def get_tmp_config(keys: List[str], default=None):
        return cfg_if.read_user_config("tmp.yaml", ["::".join(keys)], default, be_quiet=True)


cfg_if = CfgIf

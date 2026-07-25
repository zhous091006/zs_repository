import datetime
import hashlib
import math
import os
import re
import shutil
import socket
import subprocess
import tarfile
import threading
import time
from typing import List


class LibFunction:
    """-------------------------------------- Basic Function ---------------------------------------------"""

    @staticmethod
    def degrees_to_radians(degrees):
        return degrees * (math.pi / 180)

    @staticmethod
    def radians_to_degrees(radians):
        return radians * (180 / math.pi)

    @staticmethod
    def set_bit_val(byte, index, value):
        """
        更改某个字节中某一位（Bit）的值

        :param byte: 准备更改的字节原值
        :param index: 待更改位的序号，从右向左0开始，0-7为一个完整字节的8个位
        :param value: 目标位预更改的值，0或1
        :returns: 返回更改后字节的值
        """
        if value:
            return byte | (1 << index)
        return byte & ~(1 << index)

    @staticmethod
    def covert_to_db(value: [int, float, complex]):
        """
        将 int, float, complex 数据类型值转换为 db 值
        """
        if value is None:
            return None
        if isinstance(value, (float, int)):
            if value > 0:
                return round(20 * math.log10(value), 3)
        if isinstance(value, complex):
            if abs(value) > 0:
                return round(20 * math.log10(abs(value)), 3)
        return 0

    @staticmethod
    def get_date_str():
        """获取当前日期（年-月-日）"""
        return time.strftime("%Y-%m-%d", time.localtime())

    @staticmethod
    def get_date_time_str(fmt="%Y-%m-%d %H:%M:%S"):
        """获取当前日期时间（年-月-日 时:分:秒）"""
        return time.strftime(fmt, time.localtime())

    @staticmethod
    def get_date_time_microsecond_str():
        """获取当前日期时间（年-月-日 时:分:秒）"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    @staticmethod
    def get_date_time_str_in_save_report(fmt="%Y-%m-%d_%H-%M-%S"):
        """获取当前日期时间（年-月-日_时-分-秒）"""
        return time.strftime(fmt, time.localtime())

    @staticmethod
    def get_time_delta(s_time: str, e_time: str) -> int:
        _start_time = datetime.datetime.strptime(s_time, '%Y-%m-%d %H:%M:%S')
        _end_time = datetime.datetime.strptime(e_time, '%Y-%m-%d %H:%M:%S')
        time_delta = _end_time - _start_time
        return int(time_delta.total_seconds())

    @staticmethod
    def copy_data(source_dir, target_dir):
        """
        将 source_dir 文件夹下的文件拷贝到 target_dir 下。
        :param source_dir: 源文件夹
        :param target_dir: 目标文件夹
        :return:
        """
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for files in os.listdir(source_dir):
            src_name = os.path.join(source_dir, files)
            dest_name = os.path.join(target_dir, files)
            if os.path.isfile(src_name):
                if not os.path.exists(dest_name):
                    shutil.copy(src_name, dest_name)
                if os.path.isfile(dest_name):
                    if lib_func_t.get_file_md5(src_name) != lib_func_t.get_file_md5(dest_name):
                        shutil.copy(src_name, dest_name)
                else:
                    shutil.copy(src_name, dest_name)
            else:
                if not os.path.isdir(dest_name):
                    os.makedirs(dest_name)
                lib_func_t.copy_data(src_name, dest_name)
        return True

    @staticmethod
    def str_to_float_list(string):
        str_list = string.split(',')
        return [float(val) for val in str_list]

    @staticmethod
    def float_arr_to_str(data_arr):
        s = ""
        for i in range(len(data_arr)):
            s += "%.12e," % data_arr[i]
        s = s.rstrip(',')
        return s

    @staticmethod
    def str_to_complex_list(string: str):
        complex_list = []
        value_list = string.strip().split(',')
        point_num = int(len(value_list) / 2)
        for i in range(point_num):
            complex_list.append(complex(float(value_list[2 * i]), float(value_list[2 * i + 1])))
        return complex_list

    @staticmethod
    def complex_arr_to_str(cplx_arr):
        s = ""
        for i in range(len(cplx_arr)):
            s += "%.12e,%.12e," % (cplx_arr[i].real, cplx_arr[i].imag)
        s = s.rstrip(',')
        return s

    @staticmethod
    def to_int(data, default=None):
        """
        将数据转换为 float
        :param data:
        :param default: 转换失败，返回此值
        :return:
        """
        try:
            return int(data)
        except ValueError:
            return default

    @staticmethod
    def to_float(data, default=None):
        """
        将数据转换为 float
        :param data:
        :param default: 转换失败，返回此值
        :return:
        """
        try:
            return float(data)
        except ValueError:
            return default

    @staticmethod
    def to_complex(data):
        """
        将数据转换为 complex
        :param data:
        :return:
        """
        try:
            return complex(data)
        except ValueError:
            return None

    @staticmethod
    def get_desktop_path():
        return os.path.join(os.path.expanduser("~"), 'Desktop')

    @staticmethod
    def parse_csv_line_text(line_text: str, sep: str = ",") -> List[str]:
        """
        将一行文本按CSV格式解析成字符串列表
        """
        line_list = line_text.split(sep)
        N = len(line_list) - 2
        i = 0
        # 取消分割由双引号括起来的分隔符
        while i <= N:
            before = line_list[i]
            after = line_list[i + 1]
            if before.lstrip().startswith("\"") and not before.rstrip().endswith(
                    "\"") and not after.lstrip().startswith("\""):
                merge_str = before + sep + after
                line_list.pop(i + 1)
                line_list[i] = merge_str
                N = len(line_list) - 2
            else:
                i += 1
        # 被双引号包围的字符串，去除双引号
        for i in range(len(line_list)):
            item = line_list[i].strip()
            if item.startswith("\"") and item.endswith("\""):
                line_list[i] = item[1:-1]
        return line_list

    """-------------------------------------- File Function ---------------------------------------------"""

    @staticmethod
    def open_folder(folder_path: str):
        return LibFunction.show_in_explorer(folder_path)

    @staticmethod
    def create_dir_path(dir_path: str) -> bool:
        """创建路径"""
        if not dir_path:
            return False
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return os.path.exists(dir_path)

    @staticmethod
    def get_file_dir(filepath: str) -> str:
        if not filepath:
            return ""
        return os.path.dirname(filepath)

    @staticmethod
    def get_file_basename(filepath: str) -> str:
        filename = os.path.basename(filepath)
        basename = filename.split('.')[0]
        return basename

    @staticmethod
    def file_rename(src_filepath, dst_filename) -> bool:
        """文件重命名
        :param src_filepath: 源文件路径
        :param dst_filename: 目标文件名
        """
        try:
            src_filepath = os.path.normpath(src_filepath)
            LibFunction.run_subprocess(cmd=f'rename "{src_filepath}" "{dst_filename}"', shell=True)
            return True
        except BaseException as e:
            print(e)
            return False

    @staticmethod
    def file_suffix_rename(src_filepath, dst_suffix):
        """文件后缀重命名
        :param src_filepath: 源文件路径
        :param dst_suffix: 目标后缀名
        """
        try:
            file_abs_path = os.path.dirname(src_filepath)
            dst_filename = lib_func_t.get_file_basename(src_filepath) + '.' + dst_suffix
            lib_func_t.file_rename(src_filepath, dst_filename)
            return f"{file_abs_path}\\{dst_filename}"
        except BaseException as e:
            print(e)
            return ""

    @staticmethod
    def is_path_existed(path: str):
        return os.path.exists(path)

    @staticmethod
    def clean_path(path: str):
        return QDir.cleanPath(path)  # 生成的路径分隔符一直是 '/'，对正则表达式友好
        # return os.path.normpath(path)

    @staticmethod
    def is_file_occupied(filepath: str) -> bool:
        """
        判断文件是否被占用
        :param filepath:
        :return:
        """
        try:
            if not os.path.exists(filepath):
                return False
            vHandle = win32file.CreateFile(filepath, win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING,
                                           win32file.FILE_ATTRIBUTE_NORMAL, None)
            if int(vHandle) == win32file.INVALID_HANDLE_VALUE:
                return True
            win32file.CloseHandle(vHandle)
            return False
        except Exception as e:
            print("is_file_occupied error:", e)
            return True

    @staticmethod
    def make_tar_gz(src_dir: str, output_file_path: str) -> bool:
        """压缩文件夹src_dir，压缩包名称为output_file_path"""
        if os.path.exists(src_dir):
            with tarfile.open(output_file_path, "w:gz") as tar:
                tar.add(src_dir, arcname=os.path.basename(src_dir))
                return True
        return False

    @staticmethod
    def extract_bin_file(bin_name, dst_dir):
        with tarfile.open(bin_name, "r:gz") as tar:
            names = tar.getnames()
            try:
                for name in names:
                    target_file_path = f"{dst_dir}\\{name}"
                    print(target_file_path)
                    if os.path.exists(target_file_path) and os.path.isfile(target_file_path):
                        os.remove(target_file_path)
                    tar.extract(name, dst_dir)
            except BaseException as e:
                print(e)

    @staticmethod
    def get_file_md5(file_name) -> str:
        """生成文件MD5码"""
        if not os.path.exists(file_name):
            print("File not exist.")
            return ""
        with open(file_name, 'rb') as f:
            m = hashlib.md5()
            while True:
                # 如果不用二进制打开文件，则需要先编码
                # data = f.read(1024).encode('utf-8')
                data = f.read(1024)  # 将文件分块读取
                if not data:
                    break
                m.update(data)
            return m.hexdigest()

    @staticmethod
    def generate_md5_file(src_file: str, dst_md5_file: str = "") -> str:
        """生成.md5后缀的MD5校验文件
        :param src_file: 源文件路径
        :param dst_md5_file: 生成的MD5文件路径，若文件路径为空，则生成在源文件同路径下
        :return True/False
        """
        md5_value = lib_func_t.get_file_md5(src_file)
        dst_file_path = dst_md5_file if dst_md5_file else f"{src_file}.md5"
        if md5_value:
            with open(dst_file_path, "w", encoding='utf-8') as f:
                f.write(md5_value)
            return dst_file_path
        return ""

    @staticmethod
    def show_in_explorer(file_path: str) -> bool:
        """
        在文件资源管理器中显示 文件/文件夹
        :return: 操作成功返回 True，失败返回 False
        """
        file_path = lib_func_t.clean_path(file_path)
        file_path = os.path.normpath(file_path)
        if LibFunction.is_path_existed(file_path):
            LibFunction.run_subprocess(cmd=f"start explorer \"{file_path}\"", shell=True)
            return True
        return False

    @staticmethod
    def decrypt_file(filepath: str) -> str:
        """
        对输入的源文件进行解密，内容写到新建的临时文件中
        注：临时文件需要自行删除
        :param filepath: 源文件路径
        :returned: 返回临时文件路径
        """
        if os.path.isfile(filepath):
            filepath = os.path.abspath(filepath)
            cmd = f"{LIB_RESOURCE_DIR}\\bat_script\\decrypt.bat \"{filepath}\""
            lib_func_t.run_subprocess(cmd)
            return filepath + ".__decrypted__"
        return ""

    @staticmethod
    def read_file_without_encryption(file: str, mode: str, encoding: str = "") -> [str, bytes, None]:
        """
        用于将加密文件的内容整体读出来
        """
        with open(file, mode) as f:
            some_data = f.read(256)
            is_encrypted = isinstance(some_data, bytes) or "esafenet" in some_data  # 判断是否为加密文件（字节数据一律认为是加密的）

        decrypted_filepath = ""

        try:
            decrypted_filepath = lib_func_t.decrypt_file(file) if is_encrypted else file
            if encoding:
                with open(decrypted_filepath, mode, encoding=encoding) as f:
                    content = f.read()
            else:
                with open(decrypted_filepath, mode) as f:
                    content = f.read()
        except BaseException as e:
            print(e)
            content = None

        if is_encrypted and decrypted_filepath:
            os.remove(decrypted_filepath)

        return content

    @staticmethod
    def file_basename_add_suffix(filepath: str, name_suffix: str) -> str:
        file_dir = lib_func_t.get_file_dir(filepath)
        basename = lib_func_t.get_file_basename(filepath)
        suffix = os.path.splitext(filepath)[-1]
        return f"{file_dir}/{basename}{name_suffix}{suffix}"

    @staticmethod
    def shutil_copyfile(source: str, target: str):
        return shutil.copyfile(source, target)

    @staticmethod
    def shutil_copy(src: str, dst: str):
        return shutil.copy(src, dst)

    @staticmethod
    def remove_folder(folder: str) -> bool:
        """
        删除文件夹
        :param folder: 文件夹路径
        :return: bool
        """
        folder = folder.replace('/', '\\')
        try:
            ret = os.system('rd /s/q "%s"' % folder)
            if ret != 0:
                return False
        except BaseException as e:
            print(e)
            return False
        return True

    @staticmethod
    def remove_file(filepath: str) -> bool:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except BaseException as e:
            print(e)
            return False
        return True

    """-------------------------------------- Others ---------------------------------------------"""

    @staticmethod
    def run_subprocess(cmd, shell=False, cwd=None):
        """
        开启命令行子进程
        """
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return subprocess.Popen(cmd, startupinfo=startupinfo, shell=shell, cwd=cwd).communicate()


lib_func_t = LibFunction


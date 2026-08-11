# -*- coding:utf-8 –*-

import os
import time

from loguru import logger

from lib.lib_thread import LibObjectThread, LibThreadWorker


class LibDebug:

    @staticmethod
    def print(*args, sep=' ', end='\n', file=None):
        print(*args, sep, end, file)

    @staticmethod
    def print_except(e: BaseException, string=""):
        from lib.lib_translation import tr
        file_name = os.path.basename(e.__traceback__.tb_frame.f_globals["__file__"])
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        error_info = (f"[{tr('Error Msg')}]: {string} \n"
                      f" -> {tr('FileName')}: {file_name} \n"
                      f" -> {tr('LineNumber')}: {e.__traceback__.tb_lineno} \n"
                      f" -> {tr('DateTime')}: {current_time} \n"
                      f" -> {tr('Expect')}: {e}")
        lib_debug_t.print_fail(error_info)

    @staticmethod
    def print_begin_end(string, begin="\n", end="\n"):
        print(begin + "~~~ " + string + " ~~~", end=end)

    @staticmethod
    def print_process(string, begin="", end="\n"):
        print(begin + "# " + string, end=end)

    @staticmethod
    def print_success(string, end="\n"):
        print("[√] " + string, end=end)
        logger.success(string)

    @staticmethod
    def print_fail(string, end="\n"):
        print("(×) " + string, end=end)
        logger.error(string)

    @staticmethod
    def print_warning(string, end="\n"):
        print("(?) " + string, end=end)
        logger.error(string)

    @staticmethod
    def print_percent(string: str, percent: int):
        """
        percent: 0 ~ 100
        """
        display_percent = percent // 2
        display_string = f"{string} |" + "|" * display_percent + " " * (50 - display_percent) + f"| {percent}%"
        if percent == 0:
            print(display_string, end="\n")
        else:
            print(f"\r{display_string}", end="\n")

    @staticmethod
    def print_running(string: str) -> LibObjectThread:
        """
        打印等待状态语句，返回一个线程对象用于停止打印
        例：
            t = lib_debug_t.print_running("waiting for close")
            => do something ...
            t.stop()
            t.join()
        """

        class Worker(LibThreadWorker):
            def run(self):
                symbol = ["=  ", " = ", "  =", " = "]
                i = 0
                while not self.is_ready_to_quit():
                    display_string = f"[{symbol[i % len(symbol)]}] {string} "
                    if i == 0:
                        print(f"{display_string}", end="")
                    else:
                        print(f"\r{display_string}", end="")
                    i += 1
                    time.sleep(0.2)
                print("\r", end="")

        t = LibObjectThread(worker_object=Worker())
        t.start()
        return t

    @staticmethod
    def split_line():
        print("————————————————————————————————————————————————————————————————————————")
        print("<HR>")

    @staticmethod
    def ignore(string):
        pass


lib_debug_t = LibDebug

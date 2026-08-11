#!/usr/bin/env python3
# -*- coding:utf-8 –*-
# -----------------------------------------------------------------------------
# Authors:        Yan.Huang
#
# Started:        08/11/2019
#
# Version:        V1.1
#
# Copyright 2013-2020 Siglent Corporation. All Rights Reserved.
# Remarks:
# -----------------------------------------------------------------------------

# python3.6
import os
import ftplib


class LibFtpTool:
    ftp = ftplib.FTP()

    def __init__(self, host, port=21):
        try:
            self.ftp.set_pasv(True)
            self.ftp.timeout = 3
            self.ftp.connect(host, port)
        except BaseException as e:
            print("@host %s connect fail" % host, e)

    def Login(self, user: str, password: str):
        self.ftp.login(user, password)

    def DownLoadFile(self, LocalFile: str, RemoteFile: str):
        """
        download single file.
        :param LocalFile: choose path that download to
        :param RemoteFile: The file you choose download
        :return:
        """
        try:
            with open(LocalFile, 'wb') as f:
                self.ftp.retrbinary('RETR ' + RemoteFile, f.write)
        except BaseException as e:
            print("@Ftp access timeout", e)
        return True

    def DownLoadFileTree(self, LocalDir, RemoteDir):
        """
        download the whole files in the dir.
        :param LocalDir:
        :param RemoteDir:
        :return:
        """
        try:
            if not os.path.exists(LocalDir):
                os.makedirs(LocalDir)
            self.ftp.cwd(RemoteDir)
            RemoteNames = self.ftp.nlst()
            for file in RemoteNames:
                Local = os.path.join(LocalDir, file)
                if file.find(".") == -1:
                    if not os.path.exists(Local):
                        os.makedirs(Local)
                    self.DownLoadFileTree(Local, file)
                else:
                    self.DownLoadFile(Local, file)
            self.ftp.cwd("..")
        except BaseException as e:
            print("@Ftp access timeout", e)

    def close(self):
        self.ftp.quit()


if __name__ == "__main__":
    ftp = LibFtpTool("10.11.14.225")
    ftp.Login('FTP', 'FTP')
    ftp.DownLoadFileTree('D:/test/test', '/factory_data')  # 从目标目录下载到本地目录d盘
    ftp.close()

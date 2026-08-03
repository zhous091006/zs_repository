# Copyright (c) 2023 Siglent Co.，Ltd. All rights reserved.
# Author  : wang-jianwei
# Date    : 2023/1/7 11:19 
# Notes   :

from PyQt5.QtWidgets import QRadioButton


class UiRadioButton(QRadioButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

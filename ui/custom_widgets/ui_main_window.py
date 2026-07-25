import os.path
from typing import Dict

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QRect, QPoint
from PyQt5.QtGui import QIcon, QCloseEvent, QResizeEvent, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QDockWidget, QActionGroup, QFrame, QHBoxLayout, QSizePolicy, QShortcut
from PyQt5.QtWinExtras import QWinTaskbarButton

from cfg.cfg_if import cfg_if
from epcore import epcore, Character
from lib.lib_char import LibChar
from lib.lib_debug import lib_debug_t
from lib.lib_translation import tr, tr_language_update
from lib.lib_type import LIB_IMAGE_DIR, LibRunningState, LibLanguageType, LibMessageLevel
from lib.lib_version import LIB_VERSION, LIB_APP_NAME
from ui.custom_widgets.buttons.ui_font_icon_button import UiFontIconButton
from ui.custom_widgets.buttons.ui_push_button import UiPushButton
from ui.custom_widgets.menu.ui_menu import UiMenu
from ui.custom_widgets.ui_custom_main_window import UiCustomMainWindow
from ui.custom_widgets.ui_dock_widget import UiDockWidget
from ui.custom_widgets.ui_label import UiLabel
from ui.custom_widgets.ui_message_box import UiMessageBox
from ui.custom_widgets.ui_tool_bar import UiToolBar, UiToolBarButton
from ui.dialogs.ui_dialog_about import UiDialogAbout
from ui.dialogs.ui_dialog_account_info import UiDialogAccountInfo
from ui.dialogs.ui_dialog_task_global_setting import UiDialogTaskGlobalSetting
from ui.dialogs.ui_dialog_testflow_registration import UiDialogTestflowRegistration
from ui.dock_widgets.ui_device_manage_area import UiDeviceManageBody, UiDeviceManageTitle
from ui.dock_widgets.ui_dock_tool_button import UiDockToolButton
from ui.dock_widgets.ui_information_area import UiInformationBody, UiInformationTitle
from ui.dock_widgets.ui_task_running_status_area import UiTaskRunningStatusBody, UiTaskRunningStatusTitle
from ui.ui_signal_manager import UiSignalManager
from ui.ui_work_area import UiWorkArea
from ui.view_model.task_model.normal.ui_task_group_model import UiTaskGroupModel
from ui.view_model.task_model.normal.ui_task_item_model import UiTaskItemModel
from ui.view_model.task_model.ui_task_manager_model import UiTaskManagerModel
from ui.view_model.ui_docks_view_model import UiDockItemModel
from ui.view_model.ui_view_model import UiViewModel


class UiMainWindow(UiCustomMainWindow):
    sig_delay_init = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{LIB_APP_NAME} ({LIB_VERSION})")

        self.__win_taskbar_button = QWinTaskbarButton(self)

        self.shortcuts = []

        self.account_box = UiAccountBox(self)

        self.top_info_box = UiTaskInfoBox(self.top_bar)

        self.status_bar = QStatusBar(self)
        self.status_bar.setSizeGripEnabled(False)
        self.setStatusBar(self.status_bar)

        self.msg_info_displayer = UiMessageInfoWidget(self)
        self.status_bar.addWidget(self.msg_info_displayer)

        self.center = UiWorkArea(self)
        self.setCentralWidget(self.center)

        self.toolbars: Dict[Qt.ToolBarArea, UiToolBar] = {}
        self.tools: Dict[str, UiDockToolButton] = {}
        self.docks: Dict[str, UiDockWidget] = {}

        self.setDockOptions(QMainWindow.AnimatedDocks)
        self.setDockNestingEnabled(False)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        self.__init_menus()
        self.__init_toolbars()
        # self.__init_tools()
        # self.__init_docks()

        self.__init_connect()

        self.sig_delay_init.emit()

    def register_window_shortcut(self, shortcut, slot_func):
        """
        注册快捷键
        :param shortcut: 快捷键组合字符串（e.g. 'Ctrl+N'）
        :param slot_func: 快捷键对应槽函数
        :return:
        """
        _shortcut = QShortcut(QKeySequence(shortcut), self)
        _shortcut.setAutoRepeat(False)
        _shortcut.setContext(Qt.WindowShortcut)
        _shortcut.activated.connect(slot_func)
        self.shortcuts.append(shortcut)

    def delay_init(self) -> None:
        self.update_dock_widgets()

        UiViewModel.get_inst().docks_view_model.set_item_active("Device", True)

    def __init_menus(self) -> None:
        """
        初始化菜单项
        :return:
        """
        # view_menu = QMenu("View", self.top_bar)
        # view_menu.addAction("Device")
        # view_menu.addAction("Information")
        _is_RD_character = epcore.verification_character(Character.RD)
        _is_PE_character = epcore.verification_character(Character.PE)
        _is_operator_character = epcore.verification_character(Character.OPERATOR)
        _is_overseas_character = epcore.verification_character(Character.OVERSEAS)

        '''Tool Menu'''
        tool_menu = UiMenu(tr("Tool") + " (&T)", self.top_bar)

        if epcore.verification_character([Character.RD, Character.PE, Character.REPAIR, Character.OVERSEAS]):
            tool_menu.addAction(QIcon(LIB_IMAGE_DIR + "/code/code-16.png"), tr("Python Console"),
                                UiSignalManager.get_inst().sig_open_python_console_page.emit)
            self.register_window_shortcut("Ctrl+`", UiSignalManager.get_inst().sig_open_python_console_page.emit)

            tool_menu.addSeparator()
            tool_menu.addAction(QIcon(LIB_IMAGE_DIR + "/debug_32.svg"), tr("SCPI Communication"),
                                UiSignalManager.get_inst().sig_open_scpi_communication_page.emit)
            tool_menu.addSeparator()

        tool_menu.addAction(tr("Line Loss Measurement"), UiSignalManager.get_inst().sig_open_line_loss_measurement_page.emit)
        tool_menu.addSeparator()
        tool_menu.addAction(tr("VNA Calibration Equipment Control"), UiSignalManager.get_inst().sig_open_vna_cali_equip_ctrl_page.emit)
        tool_menu.addAction(tr("VNA PV Equipment Control"), UiSignalManager.get_inst().sig_open_vna_pv_equip_ctrl_page.emit)
        tool_menu.addAction(tr("VNA CALI PV MIXED Equipment Control"), UiSignalManager.get_inst().sig_open_vna_cali_pv_mixed_equip_ctrl_page.emit)

        if _is_RD_character:
            tool_menu.addSeparator()
            tool_menu.addAction(QIcon(LIB_IMAGE_DIR + "/license-64.png"), tr("Application for Option License"),
                                UiSignalManager.get_inst().sig_open_vna_option_license_application_page.emit)
            tool_menu.addSeparator()
            tool_menu.addAction(tr("License Operation (R&&D Internal Use)"),
                                UiSignalManager.get_inst().sig_open_vna_license_operation_page.emit)

        self.top_bar.addMenu(tool_menu)

        '''Setting Menu'''
        setting_menu = UiMenu(tr("Setting") + " (&S)", self.top_bar)
        setting_menu.addAction(tr("Task Settings..."), UiDialogTaskGlobalSetting.show_dialog)
        setting_menu.addSeparator()
        language_setting_menu = UiMenu(tr("Language"), self.top_bar)
        action_group = QActionGroup(self.top_bar)
        self.language_auto_action = language_setting_menu.addAction(tr("Auto"), lambda: self.set_language(LibLanguageType.AUTO))
        self.language_zh_action = language_setting_menu.addAction(tr("Chinese"), lambda: self.set_language(LibLanguageType.CHINESE))
        self.language_en_action = language_setting_menu.addAction(tr("English"), lambda: self.set_language(LibLanguageType.ENGLISH))
        self.language_auto_action.setCheckable(True)
        self.language_zh_action.setCheckable(True)
        self.language_en_action.setCheckable(True)
        action_group.addAction(self.language_auto_action)
        action_group.addAction(self.language_zh_action)
        action_group.addAction(self.language_en_action)
        language = cfg_if.get_language_type()
        if language == LibLanguageType.AUTO:
            self.language_auto_action.setChecked(True)
        elif language == LibLanguageType.CHINESE:
            self.language_zh_action.setChecked(True)
        elif language == LibLanguageType.ENGLISH:
            self.language_en_action.setChecked(True)

        setting_menu.addMenu(language_setting_menu)

        self.top_bar.addMenu(setting_menu)

        '''Advance Menu'''
        if _is_RD_character or _is_PE_character:
            adv_menu = UiMenu(tr("Advance") + " (&A)", self.top_bar)
            adv_menu.addAction(tr("Testflow Registration..."), UiDialogTestflowRegistration.show_dialog)
            adv_menu.addAction(tr("Equipment Management"), UiSignalManager.get_inst().sig_open_equipment_manage_page.emit)

            self.top_bar.addMenu(adv_menu)

        '''Help Menu'''
        help_menu = UiMenu(tr("Help") + " (&H)", self.top_bar)
        help_menu.addAction(tr("About..."), UiDialogAbout.show_dialog)

        self.top_bar.addMenu(help_menu)

    def __init_toolbars(self) -> None:
        right_tool_bar = UiToolBar("Right Tool Bar", self)
        right_tool_bar.setObjectName("RightEdge")
        right_tool_bar.setMovable(False)

        left_tool_bar = UiToolBar("Left Tool Bar", self)
        left_tool_bar.setObjectName("LeftEdge")
        left_tool_bar.setMovable(False)

        bottom_tool_bar = UiToolBar("Bottom Tool Bar", self)
        bottom_tool_bar.setObjectName("BottomEdge")
        bottom_tool_bar.setMovable(False)

        # self.addToolBar(Qt.TopToolBarArea, top_tool_bar)
        self.addToolBar(Qt.RightToolBarArea, right_tool_bar)
        self.addToolBar(Qt.BottomToolBarArea, bottom_tool_bar)
        self.addToolBar(Qt.LeftToolBarArea, left_tool_bar)

        # self.toolbars[Qt.TopToolBarArea] = top_tool_bar
        self.toolbars[Qt.RightToolBarArea] = right_tool_bar
        self.toolbars[Qt.BottomToolBarArea] = bottom_tool_bar
        self.toolbars[Qt.LeftToolBarArea] = left_tool_bar

    def __init_connect(self) -> None:
        self.sig_delay_init.connect(self.delay_init, Qt.QueuedConnection)
        UiViewModel.get_inst().docks_view_model.sig_update_ui.connect(self.update_dock_widgets)
        UiSignalManager.get_inst().sig_update_win_taskbar_progress.connect(self.__update_win_taskbar_progress_status)
        UiSignalManager.get_inst().sig_do_self_test.connect(self.do_self_test)
        self.top_info_box.sig_updated.connect(self.update_top_info_box_geometry)

    def update_dock_widgets(self) -> None:
        for dock_area, items in UiViewModel.get_inst().docks_view_model.items.items():
            for model in items[0]:
                tool_bar_btn = self.__create_tool_bar_button(model)
                dock_widget = self.__create_dock_widget(model)
                self.toolbars[dock_area].insert_widget(tool_bar_btn, 0, -1)
                self.docks[model.name] = dock_widget
                self.tools[model.name] = tool_bar_btn
            for model in items[1]:
                tool_bar_btn = self.__create_tool_bar_button(model)
                dock_widget = self.__create_dock_widget(model)
                self.toolbars[dock_area].insert_widget(tool_bar_btn, 1, -1)
                self.docks[model.name] = dock_widget
                self.tools[model.name] = tool_bar_btn

    def __create_tool_bar_button(self, model: UiDockItemModel) -> UiDockToolButton:
        if model.name in self.tools:
            return self.tools[model.name]
        btn = UiDockToolButton(QIcon(LIB_IMAGE_DIR + "/app_logo_gray.svg"), None)
        btn.set_model(model)
        dock_area = UiViewModel.get_inst().docks_view_model.get_dock_area(model)
        if dock_area == Qt.LeftDockWidgetArea:
            btn.set_text_rotate_direction(UiToolBarButton.TEXT_CLOCKWISE_ROTATE_270)
        elif dock_area == Qt.RightDockWidgetArea:
            btn.set_text_rotate_direction(UiToolBarButton.TEXT_CLOCKWISE_ROTATE_90)
        elif dock_area == Qt.BottomDockWidgetArea:
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        return btn

    def __create_dock_widget(self, model: UiDockItemModel) -> UiDockWidget:
        if model.name in self.docks:
            return self.docks[model.name]
        dock = UiDockWidget(self)
        dock.setFeatures(QDockWidget.DockWidgetMovable)
        if model.name == "Device":
            dock.setMinimumWidth(350)
            dock.setMinimumHeight(200)
            title_bar = UiDeviceManageTitle(dock)
            body = UiDeviceManageBody(dock)
        elif model.name == "Information":
            dock.setMinimumWidth(360)
            dock.setMinimumHeight(100)
            title_bar = UiInformationTitle(dock)
            body = UiInformationBody(dock)
        elif model.name == "Task Running Status":
            dock.setMinimumWidth(100)
            dock.setMinimumHeight(220)
            title_bar = UiTaskRunningStatusTitle(dock)
            body = UiTaskRunningStatusBody(dock)
        else:
            title_bar = None
            body = None

        if title_bar:
            dock.set_title_bar_widget(title_bar)
        if body:
            dock.set_body_widget(body)

        dock.set_model(model)
        return dock

    def update_account_box_geometry(self):
        r = QRect(0, 0, int(self.account_box.sizeHint().width() * 1.1), self.top_bar.height())
        r.moveTopRight(self.top_right_tool.geometry().topLeft() + QPoint(-12, 0))
        self.account_box.setGeometry(r)

    def update_top_info_box_geometry(self):
        r = QRect(QPoint(0, 0), self.top_info_box.sizeHint())
        r.moveCenter(self.top_bar.rect().center())
        self.top_info_box.setGeometry(r)

    def closeEvent(self, event: QCloseEvent) -> None:
        session_dict = UiTaskManagerModel.get_inst().get_session_dict()
        if session_dict:
            ret = UiMessageBox.warning("Warning", tr("The tasks is in progress.\nDo you still want to close the window?"),
                                       [UiMessageBox.YES_ROLE, UiMessageBox.NO_ROLE], UiMessageBox.NO_ROLE)
            if not ret:
                event.ignore()
                return
        if epcore.test_db_connect():
            epcore.sign_out()
        super().closeEvent(event)

        # for task in session_dict.values():
        #     UiTaskManagerModel.get_inst().kill_task(task)
        # while True:
        #     if not session_dict:
        #         UiViewModel.get_inst().recover_std()
        #         sys.exit()
        #     time.sleep(0.02)
        #     qApp.processEvents(QEventLoop.ExcludeUserInputEvents)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.__win_taskbar_button.setWindow(self.windowHandle())
        self.update_account_box_geometry()
        self.update_top_info_box_geometry()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.update_account_box_geometry()
        self.update_top_info_box_geometry()

    def set_language(self, language) -> None:
        if cfg_if.get_language_type() != language:
            session_dict = UiTaskManagerModel.get_inst().get_session_dict()
            if session_dict:
                UiMessageBox.warning(text=(tr("The following tasks are running, please stop these tasks first.") +
                                           "\n\n" +
                                           "\n".join([f"{i + 1}. {task_model.task_name.value}" for i, task_model in enumerate(session_dict.values())])),
                                     roles=[UiMessageBox.ACCEPT_ROLE])
                return
            cfg_if.set_language_type(language)
            if UiMessageBox.question(text=tr("Restart app window now?"), parent=self):
                UiSignalManager.get_inst().sig_restart_main_window.emit()
            tr_language_update()

    def do_self_test(self):
        """程序启动后自检"""
        # 1. 检查 任务配置 路径是否有效
        try:
            if epcore.verification_character(Character.OVERSEAS):
                ok = os.path.isdir(cfg_if.get_local_upload_data_root_path())
            else:
                ok = bool(cfg_if.get_local_upload_data_root_path() and
                          cfg_if.get_local_upload_success_backup_root_path() and
                          cfg_if.get_easy_certificate_path() and
                          cfg_if.get_pretest_report_path() and
                          cfg_if.get_aging_test_report_path() and
                          cfg_if.get_calibration_report_path() and
                          cfg_if.get_pv_report_path() and
                          cfg_if.get_sn_id_report_path())

                ok = ok & (os.path.isdir(cfg_if.get_local_upload_data_root_path()) and
                           os.path.isdir(cfg_if.get_local_upload_success_backup_root_path()) and
                           os.path.isfile(cfg_if.get_easy_certificate_path())
                           )
        except Exception as e:
            lib_debug_t.print_fail(f"Error!,Exception:{e}")
            ok = False
        if not ok:
            self.status_bar.show()
            self.msg_info_displayer.set_message(LibMessageLevel.Error,
                                                tr("Invalid configuration exists in the task settings, please configure the relevant settings correctly. "
                                                   "( Menu → Setting → Task Settings... )"))
        else:
            self.status_bar.hide()
            self.msg_info_displayer.clear_message()

    @pyqtSlot()
    def __update_win_taskbar_progress_status(self) -> None:
        """更新任务执行状态UI"""
        session_dict = UiTaskManagerModel.get_inst().get_session_dict()
        if session_dict:
            task_model = list(session_dict.values())[0]
            if isinstance(task_model, UiTaskItemModel) and isinstance(task_model.group_model, UiTaskGroupModel):
                task_model = task_model.group_model
            self.__win_taskbar_button.progress().setRange(0, 100)
            self.__win_taskbar_button.progress().setVisible(True)
            self.__win_taskbar_button.progress().setValue(int(task_model.progress.lately_progress_percent()))
            if task_model.running_state == LibRunningState.DROP_OUT:
                self.__win_taskbar_button.progress().setRange(0, 0)
        else:
            self.__win_taskbar_button.progress().setRange(0, 100)
            self.__win_taskbar_button.progress().setVisible(False)


class UiMessageInfoWidget(UiLabel):
    def set_message(self, level: LibMessageLevel, text: str):
        if level == LibMessageLevel.Error:
            self.setText(f"<span style='color:red; font-size:16px;'> ⚠ </span><span style='color:#fff'> {text} </span>")
        else:
            self.setText(text)

    def clear_message(self):
        self.clear()


class UiTaskInfoBox(QFrame):
    sig_updated = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.state = UiLabel(LibChar.ROCKET, self)
        self.state.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.text = UiLabel(self)
        self.text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.kill_task_btn = UiFontIconButton(UiFontIconButton.CLOSE, self)
        self.kill_task_btn.setObjectName("CloseBtn")
        # self.kill_task_btn.setFixedSize(12, 12)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(2)
        h_layout.addWidget(self.state)
        h_layout.addWidget(self.text)
        h_layout.addWidget(self.kill_task_btn)

        self.setLayout(h_layout)

        self.__init_connect()

        self.update_info()

    def __init_connect(self):
        UiTaskManagerModel.get_inst().sig_update_ui.connect(self.update_info)
        self.kill_task_btn.clicked.connect(self.kill_task)

    @pyqtSlot()
    def kill_task(self):
        session_dict = UiTaskManagerModel.get_inst().get_session_dict()
        if session_dict:
            task_model = list(session_dict.values())[0]
            if isinstance(task_model, UiTaskItemModel) and isinstance(task_model.group_model, UiTaskGroupModel):
                task_model = task_model.group_model
            task_model.kill()

    @pyqtSlot()
    def update_info(self):
        """
        更新任务信息
        :return:
        """
        session_dict = UiTaskManagerModel.get_inst().get_session_dict()
        if session_dict:
            task_model = list(session_dict.values())[0]
            if isinstance(task_model, UiTaskItemModel) and isinstance(task_model.group_model, UiTaskGroupModel):
                task_model = task_model.group_model
            self.text.setText(task_model.task_name.value)
            self.setVisible(True)
        else:
            self.text.setText("")
            self.setVisible(False)
        self.sig_updated.emit()


class UiAccountBox(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.user_avatar = UiPushButton(LibChar.SMILING_FACE, self)
        self.user_avatar.setObjectName("UserAvatar")
        self.user_avatar.setFixedSize(24, 24)

        self.username = UiPushButton("", self)
        self.username.setObjectName("Username")

        self.h_layout = QHBoxLayout()
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.setSpacing(4)
        self.h_layout.addWidget(self.user_avatar)
        self.h_layout.addWidget(self.username)

        self.setLayout(self.h_layout)

        self.username.setText(epcore.get_username().replace("&", "&&"))

        self.__init_connect()

    def __init_connect(self):
        self.username.clicked.connect(UiDialogAccountInfo.show_dialog)

    """
    def sign_in(self):
        # db_basic.sign_in(username="Siglent Overseas Engineer", password="❤")
        db_basic.sign_in(username="Siglent R&D Engineer", password="❤❤❤")

    def sign_out(self):
        db_basic.sign_out()
    """

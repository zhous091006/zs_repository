import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QGroupBox, QStyleFactory
)
from PyQt5.QtCore import Qt

from ui.custom_widgets.inputs.ui_line_edit import UiLineEdit


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UiLineEdit 功能演示")
        self.resize(500, 650)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # IP 地址校验
        grp_ip = QGroupBox("IP 地址 (CHECK_IP)")
        ip_layout = QVBoxLayout()
        self.ip_edit = UiLineEdit()
        self.ip_edit.set_validity_check(UiLineEdit.CHECK_IP)
        self.ip_edit.setPlaceholderText("例如: 192.168.1.1")
        ip_layout.addWidget(self.ip_edit)
        self.ip_status = QLabel("状态: 请输入IP地址")
        ip_layout.addWidget(self.ip_status)
        grp_ip.setLayout(ip_layout)

        # 端口号校验
        grp_port = QGroupBox("端口号 (CHECK_PORT)")
        port_layout = QVBoxLayout()
        self.port_edit = UiLineEdit()
        self.port_edit.set_validity_check(UiLineEdit.CHECK_PORT)
        self.port_edit.setPlaceholderText("例如: 8080")
        port_layout.addWidget(self.port_edit)
        self.port_status = QLabel("状态: 请输入端口号")
        port_layout.addWidget(self.port_status)
        grp_port.setLayout(port_layout)

        # 文件路径校验
        grp_file = QGroupBox("文件路径 (CHECK_FILE)")
        file_layout = QVBoxLayout()
        self.file_edit = UiLineEdit()
        self.file_edit.set_validity_check(UiLineEdit.CHECK_FILE)
        self.file_edit.setPlaceholderText("例如: C:\\test\\file.txt")
        file_layout.addWidget(self.file_edit)
        self.file_status = QLabel("状态: 请输入文件路径")
        file_layout.addWidget(self.file_status)
        grp_file.setLayout(file_layout)

        # 真实文件校验
        grp_realfile = QGroupBox("真实文件 (CHECK_REAL_FILE)")
        realfile_layout = QVBoxLayout()
        self.realfile_edit = UiLineEdit()
        self.realfile_edit.set_validity_check(UiLineEdit.CHECK_REAL_FILE)
        self.realfile_edit.setPlaceholderText("例如: C:\\Windows\\system.ini")
        realfile_layout.addWidget(self.realfile_edit)
        self.realfile_status = QLabel("状态: 请输入存在的文件路径")
        realfile_layout.addWidget(self.realfile_status)
        grp_realfile.setLayout(realfile_layout)

        # 目录路径校验
        grp_dir = QGroupBox("目录路径 (CHECK_DIR)")
        dir_layout = QVBoxLayout()
        self.dir_edit = UiLineEdit()
        self.dir_edit.set_validity_check(UiLineEdit.CHECK_DIR)
        self.dir_edit.setPlaceholderText("例如: C:\\Windows")
        dir_layout.addWidget(self.dir_edit)
        self.dir_status = QLabel("状态: 请输入目录路径")
        dir_layout.addWidget(self.dir_status)
        grp_dir.setLayout(dir_layout)

        # 数字校验
        grp_number = QGroupBox("数字 (CHECK_NUMBER)")
        number_layout = QVBoxLayout()
        self.number_edit = UiLineEdit()
        self.number_edit.set_validity_check(UiLineEdit.CHECK_NUMBER)
        self.number_edit.setPlaceholderText("例如: 12345")
        number_layout.addWidget(self.number_edit)
        self.number_status = QLabel("状态: 请输入数字")
        number_layout.addWidget(self.number_status)
        grp_number.setLayout(number_layout)

        # 序列号校验
        grp_serial = QGroupBox("序列号 (CHECK_SERIAL_NUMBER)")
        serial_layout = QVBoxLayout()
        self.serial_edit = UiLineEdit()
        self.serial_edit.set_validity_check(UiLineEdit.CHECK_SERIAL_NUMBER)
        self.serial_edit.setPlaceholderText("例如: ABC123-XYZ")
        serial_layout.addWidget(self.serial_edit)
        self.serial_status = QLabel("状态: 请输入序列号")
        serial_layout.addWidget(self.serial_status)
        grp_serial.setLayout(serial_layout)

        layout.addWidget(grp_ip)
        layout.addWidget(grp_port)
        layout.addWidget(grp_file)
        layout.addWidget(grp_realfile)
        layout.addWidget(grp_dir)
        layout.addWidget(grp_number)
        layout.addWidget(grp_serial)
        layout.addStretch()

        # 绑定信号
        self.ip_edit.editingFinished.connect(lambda: self.update_status(self.ip_status, self.ip_edit))
        self.port_edit.editingFinished.connect(lambda: self.update_status(self.port_status, self.port_edit))
        self.file_edit.editingFinished.connect(lambda: self.update_status(self.file_status, self.file_edit))
        self.realfile_edit.editingFinished.connect(lambda: self.update_status(self.realfile_status, self.realfile_edit))
        self.dir_edit.editingFinished.connect(lambda: self.update_status(self.dir_status, self.dir_edit))
        self.number_edit.editingFinished.connect(lambda: self.update_status(self.number_status, self.number_edit))
        self.serial_edit.editingFinished.connect(lambda: self.update_status(self.serial_status, self.serial_edit))

    def update_status(self, label: QLabel, edit: UiLineEdit):
        is_valid = edit.is_content_valid()
        label.setText(f"状态: {'有效' if is_valid else '无效'}")


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    win = DemoWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

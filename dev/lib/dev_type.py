from enum import Enum
from typing import Set, List, Dict

from lib.lib_func import lib_func_t
from lib.lib_type import LibVnaVersionType


class DevType(Enum):
    ANY_DEVICE = "Any Device"
    VNA = "VNA"
    PME = "PME"
    SA = "SA"
    VNA_CALI_EQUIPMENT = "VNA Calibration Equipment"
    VNA_PV_EQUIPMENT = "VNA PV Equipment"
    VNA_CALI_PV_MIXED_EQUIPMENT = "VNA Calibration PV Mixed Equipment"
    SDG = "SDG"
    SDM = "SDM"
    SIGLENT_ECAL = "Siglent ECal"

    @staticmethod
    def from_str(s) -> 'DevType':
        for it in DevType:
            if it.value == s:
                return it
        raise ValueError(s)

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(f'!{cls.__name__}', node.value)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value)


class DevConnectMode(Enum):
    USB = "USB"
    USB_DISCOVERY_MODE = "USB (Discovery Mode)"  # 通过 USB 的连接，读取机器有效信息（除了 IDN 提供的信息），判断是否为有效连接
    LAN = "LAN"  # 只需要IP地址
    SOCKET = "Raw Socket"  # 原始Socket通信，需要IP地址和端口号
    VISA_RESOURCE_NAME = "Visa Resource Name"

    @staticmethod
    def from_str(s) -> 'DevConnectMode':
        for it in DevConnectMode:
            if it.value == s:
                return it
        raise ValueError(s)

    @staticmethod
    def get_dev_assigned_connect_modes(dev_type: DevType) -> List['DevConnectMode']:
        assigned_connect_mode_dict = {
            DevType.ANY_DEVICE: [DevConnectMode.USB, DevConnectMode.USB_DISCOVERY_MODE, DevConnectMode.LAN, DevConnectMode.SOCKET, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.VNA: [DevConnectMode.USB, DevConnectMode.LAN, DevConnectMode.SOCKET, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.PME: [DevConnectMode.USB, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.SA: [DevConnectMode.USB, DevConnectMode.LAN, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.VNA_CALI_EQUIPMENT: [DevConnectMode.USB, DevConnectMode.USB_DISCOVERY_MODE, DevConnectMode.LAN, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.VNA_PV_EQUIPMENT: [DevConnectMode.USB, DevConnectMode.USB_DISCOVERY_MODE, DevConnectMode.LAN, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.VNA_CALI_PV_MIXED_EQUIPMENT: [DevConnectMode.USB, DevConnectMode.USB_DISCOVERY_MODE, DevConnectMode.LAN, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.SIGLENT_ECAL: [DevConnectMode.USB, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.SDG: [DevConnectMode.USB, DevConnectMode.LAN, DevConnectMode.VISA_RESOURCE_NAME],
            DevType.SDM: [DevConnectMode.USB, DevConnectMode.LAN, DevConnectMode.VISA_RESOURCE_NAME],
        }
        return assigned_connect_mode_dict[dev_type]

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(f'!{cls.__name__}', node.value)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value)


class DevError(Enum):
    OK = "ok"  # 无错误
    UNKNOWN_ERROR = "unknown_error"  # 未知错误
    TIMEOUT = "timeout"  # 设备通信超时
    SYSTEM_ERROR = "system_error"  # VI_ERROR_SYSTEM_ERROR (-1073807360): Unknown system error (miscellaneous error).
    DEVICE_NOT_EXISTED = "device_not_existed"  # 设备列表中不存在相关类型的设备
    TAGS_NOT_MATCH = "tags_not_match"  # 设备列表中不存在指定标签的设备
    DEVICE_NOT_CONNECTED = "device_not_connected"  # 存在相关设备，但设备未连接
    INVALID_COMMAND = "invalid_command"  # 非法指令


class DevScpiCmdPacket:
    def __init__(self, cmd, timeout, read_raw_size=1024,
                 values=None, datatype="f", is_big_endian=False,
                 container=bytearray, chunk_size=None):
        self.cmd = cmd
        self.timeout = timeout
        self.read_raw_size = read_raw_size  # 执行 read raw 时需要指定大小

        # used for binary_values
        self.values = values
        self.datatype = datatype
        self.is_big_endian = is_big_endian
        self.container = container
        self.chunk_size = chunk_size


class DevScpiReplyPacket:
    def __init__(self, error: DevError = None, data=None, dev_index: int = -1):
        self.error: DevError = error
        self.dev_index: int = dev_index
        self.data = data

    def __str__(self) -> str:
        return f"DevScpiReplyPacket(error={self.error}, dev_index={self.dev_index}, data={self.data})"


class DevConnectStatusType(Enum):
    CONNECTING = "Connecting"
    NOT_CONNECTED = "Not Connected"
    TCPIP = "TCPIP"
    USB = "USB"
    TELNET = "Telnet"

    @staticmethod
    def is_connected(connect_status) -> bool:
        return connect_status not in (DevConnectStatusType.NOT_CONNECTED, DevConnectStatusType.CONNECTING)


class DevConfigModel:
    """
    name: Device's name.
    type: VNA[Vector network analyzer], PME[Power Meter], SSM[Siglent SM], SA[Spectrum Analyzer]
    tags: Tags used to describe the purpose of the device.
    fixed: Fixed devices cannot be removed from the configuration, and names, types, and labels cannot be modified.
    enable: Mark whether the device is enabled.
    connect_mode_select: Device's connect mode.
    """

    def __init__(self, **kwargs):
        self.index: int = kwargs.get("index", -1)
        self.name: str = kwargs.get("name", "")
        self.type: DevType = kwargs.get("type", DevType.ANY_DEVICE)
        self.tags: Set[str] = kwargs.get("tags", set())
        self.fixed: bool = kwargs.get("fixed", False)
        self.enable: bool = kwargs.get("enable", True)
        self.visible: bool = kwargs.get("visible", True)
        self.connect_mode_options: List[DevConnectMode] = DevConnectMode.get_dev_assigned_connect_modes(self.type)

        self.connect_mode_select: DevConnectMode = self.connect_mode_options[0] if self.connect_mode_options else None
        if v := kwargs.get("connect_mode_select", None):
            self.set_connect_mode(v)

        self.connect_param_ip: str = kwargs.get("connect_param_ip", "") if (DevConnectMode.LAN in self.connect_mode_options or DevConnectMode.SOCKET in self.connect_mode_options) else ""
        self.connect_param_port: str = kwargs.get("connect_param_port", "5025") if (DevConnectMode.SOCKET in self.connect_mode_options) else "5025"
        self.connect_param_manufacturer: str = kwargs.get("connect_param_manufacturer", "") if (DevConnectMode.USB in self.connect_mode_options) else ""
        self.connect_param_model: str = kwargs.get("connect_param_model", "") if (DevConnectMode.USB in self.connect_mode_options) else ""
        self.connect_param_serial_number: str = kwargs.get("connect_param_serial_number", "") if (DevConnectMode.USB in self.connect_mode_options) else ""
        self.connect_param_version: str = kwargs.get("connect_param_version", "") if (DevConnectMode.USB in self.connect_mode_options) else ""
        self.connect_param_discovery_cmd: str = kwargs.get("connect_param_discovery_cmd", "") if (DevConnectMode.USB_DISCOVERY_MODE in self.connect_mode_options) else ""
        self.connect_param_discovery_name: str = kwargs.get("connect_param_discovery_name", "") if (DevConnectMode.USB_DISCOVERY_MODE in self.connect_mode_options) else ""
        self.connect_param_visa_res_name: str = kwargs.get("connect_param_visa_res_name", "")

    def reset(self):
        self.index = -1
        self.name = ""
        self.type = DevType.VNA
        self.tags = set()
        self.fixed = False
        self.enable = True
        self.visible = True
        self.connect_mode_options = []
        self.connect_mode_select = DevConnectMode.USB
        self.connect_param_ip = ""
        self.connect_param_port = ""
        self.connect_param_manufacturer = ""
        self.connect_param_model = ""
        self.connect_param_serial_number = ""
        self.connect_param_version = ""
        self.connect_param_discovery_cmd = ""
        self.connect_param_discovery_name = ""
        self.connect_param_visa_res_name = ""

    def set_name(self, name: str) -> None:
        self.name = name

    def set_tags(self, tags: Set[str]) -> None:
        self.tags = tags

    def set_type(self, dev_type: DevType) -> None:
        self.type = dev_type
        self.connect_mode_options = DevConnectMode.get_dev_assigned_connect_modes(self.type)
        if self.connect_mode_select not in self.connect_mode_options:
            self.connect_mode_select = self.connect_mode_options[0]

    def set_fixed(self, fixed: bool) -> None:
        self.fixed = fixed

    def set_enabled(self, enable: bool) -> None:
        self.enable = enable

    def set_visible(self, visible: bool) -> None:
        self.visible = visible

    def set_connect_options(self, options: List[DevConnectMode]):
        t_connect_mode = self.connect_mode_select
        self.connect_mode_options = options
        self.set_connect_mode(t_connect_mode)

    def set_connect_mode(self, mode: DevConnectMode) -> bool:
        if mode in self.connect_mode_options:
            self.connect_mode_select = mode
            return True

        if len(self.connect_mode_options) > 0:
            self.connect_mode_select = self.connect_mode_options[0]
        else:
            self.connect_mode_select = None
        return False

    def set_connect_param(self, **kwargs) -> None:
        if v := kwargs.get("ip"):
            self.connect_param_ip = v
        if v := kwargs.get("port"):
            self.connect_param_port = v
        if v := kwargs.get("manufacturer"):
            self.connect_param_manufacturer = v
        if v := kwargs.get("model"):
            self.connect_param_model = v
        if v := kwargs.get("serial_number"):
            self.connect_param_serial_number = v
        if v := kwargs.get("version"):
            self.connect_param_version = v
        if v := kwargs.get("discovery_cmd"):
            self.connect_param_discovery_cmd = v
        if v := kwargs.get("discovery_name"):
            self.connect_param_discovery_name = v
        if v := kwargs.get("visa_res_name"):
            self.connect_param_visa_res_name = v

    @staticmethod
    def tags_to_str(tags: Set[str], sep: str = ', ') -> str:
        return sep.join(lib_func_t.list_sort(list(tags)))

    @staticmethod
    def str_to_tags(tags_str: str, sep: str = ',') -> Set[str]:
        return {x.strip() for x in tags_str.split(sep)}

    def load(self, dev_config: dict) -> bool:
        """
        加载配置信息
        :param dev_config: 设备配置
        :return:
        """
        if not isinstance(dev_config, dict):
            return False

        self.reset()
        try:
            dev_index = dev_config.get("dev_index", self.index)
            if dev_index < 0:
                return False

            self.index = dev_index
            self.set_name(dev_config["name"])
            self.set_type(dev_config["type"])
            self.set_tags(set(dev_config["tags"]))
            self.set_fixed(dev_config.get("fixed", False))
            self.set_enabled(dev_config.get("enable", True))
            self.set_visible(dev_config.get("visible", True))
            self.set_connect_options(dev_config.get("connect_mode_options"))
            self.set_connect_mode(dev_config.get("connect_mode_select"))
            self.set_connect_param(ip=dev_config.get("connect_param_ip"),
                                   port=dev_config.get("connect_param_port"),
                                   manufacturer=dev_config.get("connect_param_manufacturer"),
                                   model=dev_config.get("connect_param_model"),
                                   serial_number=dev_config.get("connect_param_serial_number"),
                                   version=dev_config.get("connect_param_version"),
                                   discovery_cmd=dev_config.get("connect_param_discovery_cmd"),
                                   discovery_name=dev_config.get("connect_param_discovery_name"),
                                   visa_res_name=dev_config.get("connect_param_visa_res_name"))
        except BaseException as e:
            print(e)
            return False

        return True

    def export(self) -> dict:
        dev_cfg = {
            "index": self.index,
            "name": self.name,
            "type": self.type,
            "tags": self.tags,
            "fixed": self.fixed,
            "enable": self.enable,
            "visible": self.visible,
            "connect_mode_options": self.connect_mode_options,
            "connect_mode_select": self.connect_mode_select,
            "connect_param_ip": self.connect_param_ip,
            "connect_param_port": self.connect_param_port,
            "connect_param_manufacturer": self.connect_param_manufacturer,
            "connect_param_model": self.connect_param_model,
            "connect_param_serial_number": self.connect_param_serial_number,
            "connect_param_version": self.connect_param_version,
            "connect_param_discovery_cmd": self.connect_param_discovery_cmd,
            "connect_param_discovery_name": self.connect_param_discovery_name,
            "connect_param_visa_res_name": self.connect_param_visa_res_name,
        }
        return dev_cfg


class DevInfoGroup:
    def __init__(self, idn: str, connect_status: DevConnectStatusType, other_info=None):
        if other_info is None:
            other_info = {}

        self.idn: str = idn
        self.connect_status: DevConnectStatusType = connect_status
        self.other_info: dict = other_info

    def is_connected(self) -> bool:
        return DevConnectStatusType.is_connected(self.connect_status)


class DevVnaInfoGroup(DevInfoGroup):
    def __init__(self, idn: str, connect_status: DevConnectStatusType, vna_version_info: Dict[LibVnaVersionType, object]):
        super().__init__(idn, connect_status)

        self.idn: str = idn
        self.connect_status: DevConnectStatusType = connect_status
        self.vna_version_info: Dict[LibVnaVersionType, object] = vna_version_info

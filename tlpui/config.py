from enum import Enum
from .uihelper import StateImage


class ConfType(Enum):
    DEFAULT = 1
    DROPIN = 2
    USER = 3
    ERR = 4


class TlpConfig:
    def __init__(self, enabled: bool, name: str, value: str, conftype: ConfType, confpath=""):
        self.enabled = enabled
        self.enabledstore = enabled
        self.name = name
        self.value = value
        self.valuestore = value
        self.conftype = conftype
        self.confpath = confpath
        self.stateimage = None      # type: StateImage

    def get_name(self) -> str:
        return self.name

    def get_conf_type(self) -> ConfType:
        return self.conftype

    def get_conf_path(self) -> str:
        return self.confpath

    def get_value(self) -> str:
        return self.value

    def set_value(self, newvalue: str):
        self.value = newvalue
        self.refresh_state_image()

    def set_enabled(self, newstate: bool):
        self.enabled = newstate
        self.refresh_state_image()

    def is_enabled(self) -> bool:
        return self.enabled

    def add_state_image(self, newstateimage: StateImage):
        self.stateimage = newstateimage
        self.refresh_state_image()

    def refresh_state_image(self):
        self.stateimage.refresh(self.value, self.valuestore, self.enabled, self.enabledstore)

from enum import Enum
from . import settings


class ConfType(Enum):
    DEFAULT = 1
    DROPIN = 2
    USER = 3
    ERR = 4


class TlpDefaults:
    def __init__(self, name: str, value: str, enabled: bool):
        self.name = name
        self.value = value
        self.enabled = enabled

    def get_name(self) -> str:
        return self.name

    def get_value(self) -> str:
        return self.value

    def is_enabled(self) -> bool:
        return self.enabled


class TlpConfig:
    def __init__(self, enabled: bool, name: str, value: str, conftype: ConfType, confpath=""):
        self.enabled = enabled
        self.enabledstore = enabled
        self.name = name
        self.value = value
        self.valuestore = value
        self.conftype = conftype
        self.confpath = confpath

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
        self.refresh_image_state()

    def set_enabled(self, newstate: bool):
        self.enabled = newstate
        self.refresh_image_state()

    def is_enabled(self) -> bool:
        return self.enabled

    def refresh_image_state(self):
        settings.imagestate[self.name].refresh_image_state(self.value, self.valuestore, self.enabled, self.enabledstore)


def get_changed_properties() -> dict:
    changedproperties = dict()

    changed = settings.tlpconfig
    original = settings.tlpconfig_original

    for configid in changed:
        config = changed[configid]              # type: TlpConfig
        config_original = original[configid]    # type: TlpConfig

        statechange = config.is_enabled() != config_original.is_enabled()
        configchange = config.get_value() != config_original.get_value()

        if statechange or configchange:
            configname = config.get_name()

            if not config.is_enabled() and settings.tlpconfig_defaults[configname].is_enabled():
                enabled = ""
                value = "* empty"
            else:
                enabled = "" if config.is_enabled() else "#"
                value = config.get_value()

            value = '\"' + value + '\"'
            changedproperties[configname] = "{}{}={}".format(enabled, configname, value)

    return changedproperties
from . import settings

class TlpConfig:
    def __init__(self, raw: str, linenumber: int, enabled: bool, name: str, value: str, quoted: bool):
        self.raw = raw
        self.linenumber = linenumber
        self.enabled = enabled
        self.enabledstore = enabled
        self.name = name
        self.value = value
        self.valuestore = value
        self.quoted = quoted

    def get_raw(self) -> str:
        return self.raw

    def get_linenumber(self) -> int:
        return self.linenumber

    def get_name(self) -> str:
        return self.name

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

    def is_quoted(self) -> bool:
        return self.quoted

    def refresh_image_state(self):
        settings.imagestate[self.name].refresh_image_state(self.value, self.valuestore, self.enabled, self.enabledstore)


def get_changed_properties() -> list:
    changedproperties = list()

    changed = settings.tlpconfig
    original = settings.tlpconfig_original

    for configid in changed:
        config = changed[configid]              # type: TlpConfig
        config_original = original[configid]    # type: TlpConfig

        statechange = config.is_enabled() != config_original.is_enabled()
        configchange = config.get_value() != config_original.get_value()

        if statechange or configchange:
            state = '#'
            if config.is_enabled():
                state = ''

            value = config.get_value()
            if config.is_quoted():
                value = '\"' + value + '\"'

            newconfigvalue = state + config.get_name() + '=' + value
            changedproperties.append([config.get_raw(), config.get_linenumber(), newconfigvalue])

    return changedproperties
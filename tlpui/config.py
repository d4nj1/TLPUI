"""TLP config."""

from enum import Enum
from .uihelper import StateImage


class ConfType(Enum):
    """Config type enum class."""

    DEFAULT = 1
    DROPIN = 2
    USER = 3
    ERR = 4


class TlpConfig:
    """TLP config class."""

    def __init__(self, enabled: bool, name: str, value: str, conftype: ConfType, confpath=""):
        """Init TLP config class parameters."""
        self.enabled = enabled
        self.enabledstore = enabled
        self.name = name
        self.value = value
        self.valuestore = value
        self.conftype = conftype
        self.confpath = confpath
        self.stateimage = None      # type: StateImage

    def get_name(self) -> str:
        """Get config name."""
        return self.name

    def get_conf_type(self) -> ConfType:
        """Get config type."""
        return self.conftype

    def get_conf_path(self) -> str:
        """Get config path."""
        return self.confpath

    def get_value(self) -> str:
        """Get config value."""
        return self.value

    def set_value(self, newvalue: str):
        """Get config value."""
        self.value = newvalue
        self.refresh_state_image()

    def set_enabled(self, newstate: bool):
        """Set config enabled."""
        self.enabled = newstate
        self.refresh_state_image()

    def is_enabled(self) -> bool:
        """Get config enabled."""
        return self.enabled

    def add_state_image(self, newstateimage: StateImage):
        """Add image with state."""
        self.stateimage = newstateimage
        self.refresh_state_image()

    def refresh_state_image(self):
        """Refresh state image."""
        self.stateimage.refresh(self.value, self.valuestore, self.enabled, self.enabledstore)

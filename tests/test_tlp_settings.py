import pytest
import linecache
import shutil
import os
from tlpui import settingshelper


@pytest.fixture
def with_broken_config(request):
    settings_path = os.path.dirname(os.path.abspath(__file__)) + '/settings_default'
    os.environ['XDG_CONFIG_HOME'] = settings_path
    userconfig = settingshelper.UserConfig()
    userconfig.userconfigfile.write_text("[default]")
    userconfig.read_user_config()

    def clean_config_file():
        shutil.rmtree(settings_path)

    request.addfinalizer(clean_config_file)
    return userconfig.userconfigfile


@pytest.fixture
def with_new_config(request):
    settings_path = os.path.dirname(os.path.abspath(__file__)) + '/settings_creation'
    os.environ['XDG_CONFIG_HOME'] = settings_path
    userconfig = settingshelper.UserConfig()

    def clean_config_file():
        shutil.rmtree(settings_path)

    request.addfinalizer(clean_config_file)
    return userconfig.userconfigfile


def test_tlp_settings_recreation(with_broken_config):
    assert linecache.getline(str(with_broken_config), 1) == "[default]\n"
    assert linecache.getline(str(with_broken_config), 2) == "language = en_EN\n"
    assert linecache.getline(str(with_broken_config), 3) == "activeoption = 0\n"
    assert linecache.getline(str(with_broken_config), 4) == "activecategory = 0\n"
    assert linecache.getline(str(with_broken_config), 5) == "activeposition = 0\n"
    assert linecache.getline(str(with_broken_config), 6) == "windowxsize = 900\n"
    assert linecache.getline(str(with_broken_config), 7) == "windowysize = 600\n"


def test_tlp_settings_creation(with_new_config):
    assert linecache.getline(str(with_new_config), 1) == "[default]\n"
    assert linecache.getline(str(with_new_config), 2) == "language = en_EN\n"
    assert linecache.getline(str(with_new_config), 3) == "activeoption = 0\n"
    assert linecache.getline(str(with_new_config), 4) == "activecategory = 0\n"
    assert linecache.getline(str(with_new_config), 5) == "activeposition = 0\n"
    assert linecache.getline(str(with_new_config), 6) == "windowxsize = 900\n"
    assert linecache.getline(str(with_new_config), 7) == "windowysize = 600\n"


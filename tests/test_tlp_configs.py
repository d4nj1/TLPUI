from tlpui.filehelper import extract_default_tlp_configs, get_yaml_schema_object_from_file
from os import path


def get_config_count(categories):
    configcount = 0
    for category in categories:
        configs = category['configs']
        for config in configs:
            if 'group' in config:
                groupitems = config['ids']
                configcount += len(groupitems)
            else:
                configcount += 1
    return configcount


class TlpConfigTest:
    jsoncategories_count = 0
    tlpconfig_count = 0
    yamlconfig_count = 0

    def __init__(self, version: str):
        tlpuipath = f"{path.dirname(path.abspath(__file__))}/../tlpui"
        jsoncategories = get_yaml_schema_object_from_file('categories', f'{tlpuipath}/configschema/{version}.yaml')
        self.jsoncategories_count = len(jsoncategories)
        self.tlpconfig_count = len(extract_default_tlp_configs(f'{tlpuipath}/defaults/tlp-{version}.conf'))
        self.yamlconfig_count = get_config_count(jsoncategories)


def test_tlp_version_1_3():
    config_test = TlpConfigTest('1_3')
    assert config_test.jsoncategories_count == 11
    assert config_test.tlpconfig_count == 99
    assert config_test.tlpconfig_count == config_test.yamlconfig_count


def test_tlp_version_1_4():
    config_test = TlpConfigTest('1_4')
    assert config_test.jsoncategories_count == 11
    assert config_test.tlpconfig_count == 107
    assert config_test.tlpconfig_count == config_test.yamlconfig_count


def test_tlp_version_1_5():
    config_test = TlpConfigTest('1_5')
    assert config_test.jsoncategories_count == 11
    assert config_test.tlpconfig_count == 107
    assert config_test.tlpconfig_count == config_test.yamlconfig_count


def test_tlp_version_1_6():
    config_test = TlpConfigTest('1_6')
    assert config_test.jsoncategories_count == 11
    assert config_test.tlpconfig_count == 109
    assert config_test.tlpconfig_count == config_test.yamlconfig_count


def test_tlp_version_1_7():
    config_test = TlpConfigTest('1_7')
    assert config_test.jsoncategories_count == 11
    assert config_test.tlpconfig_count == 106
    assert config_test.tlpconfig_count == config_test.yamlconfig_count
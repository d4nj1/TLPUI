import unittest
from tlpui.filehelper import extract_default_tlp_configs, get_json_schema_object_from_file
from os import path

tlpuipath = f"{path.dirname(path.abspath(__file__))}/../tlpui"


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
    jsonconfig_count = 0

    def __init__(self, version: str):
        jsoncategories = get_json_schema_object_from_file('categories', f'{tlpuipath}/configschema/{version}.json')
        self.jsoncategories_count = len(jsoncategories)
        self.tlpconfig_count = len(extract_default_tlp_configs(f'{tlpuipath}/defaults/tlp-{version}.conf'))
        self.jsonconfig_count = get_config_count(jsoncategories)


class MyTestCase(unittest.TestCase):

    def test_tlp_version_0_8(self):
        config_test = TlpConfigTest('0_8')
        assert config_test.jsoncategories_count == 11
        assert config_test.tlpconfig_count == 80
        assert config_test.tlpconfig_count == config_test.jsonconfig_count

    def test_tlp_version_0_9(self):
        config_test = TlpConfigTest('0_9')
        assert config_test.jsoncategories_count == 11
        assert config_test.tlpconfig_count == 84
        assert config_test.tlpconfig_count == config_test.jsonconfig_count

    def test_tlp_version_1_0(self):
        config_test = TlpConfigTest('1_0')
        assert config_test.jsoncategories_count == 11
        assert config_test.tlpconfig_count == 90
        assert config_test.tlpconfig_count == config_test.jsonconfig_count

    def test_tlp_version_1_1(self):
        config_test = TlpConfigTest('1_1')
        assert config_test.jsoncategories_count == 11
        assert config_test.tlpconfig_count == 91
        assert config_test.tlpconfig_count == config_test.jsonconfig_count

    def test_tlp_version_1_2(self):
        config_test = TlpConfigTest('1_2')
        assert config_test.jsoncategories_count == 11
        assert config_test.tlpconfig_count == 100
        assert config_test.tlpconfig_count == config_test.jsonconfig_count

    def test_tlp_version_1_3(self):
        config_test = TlpConfigTest('1_3')
        assert config_test.jsoncategories_count == 11
        assert config_test.tlpconfig_count == 99
        assert config_test.tlpconfig_count == config_test.jsonconfig_count

    def test_tlp_version_1_4(self):
        config_test = TlpConfigTest('1_4')
        assert config_test.jsoncategories_count == 11
        assert config_test.tlpconfig_count == 107
        assert config_test.tlpconfig_count == config_test.jsonconfig_count

    def test_tlp_version_1_5(self):
        config_test = TlpConfigTest('1_5')
        assert config_test.jsoncategories_count == 11
        assert config_test.tlpconfig_count == 107
        assert config_test.tlpconfig_count == config_test.jsonconfig_count


if __name__ == '__main__':
    unittest.main()

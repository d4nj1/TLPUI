import unittest
from tlpui.filehelper import extract_default_tlp_configs, get_json_schema_object_from_file


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


class MyTestCase(unittest.TestCase):

    def test_tlp_version_0_8(self):
        version = "0_8"
        tlpconfig_defaults = extract_default_tlp_configs('../tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', '../tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        assert len(jsoncategories) == 11
        assert len(tlpconfig_defaults) == 80
        assert len(tlpconfig_defaults) == jsonconfigcount

    def test_tlp_version_0_9(self):
        version = "0_9"
        tlpconfig_defaults = extract_default_tlp_configs('../tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', '../tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        assert len(jsoncategories) == 11
        assert len(tlpconfig_defaults) == 84
        assert len(tlpconfig_defaults) == jsonconfigcount

    def test_tlp_version_1_0(self):
        version = "1_0"
        tlpconfig_defaults = extract_default_tlp_configs('../tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', '../tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        assert len(jsoncategories) == 11
        assert len(tlpconfig_defaults) == 90
        assert len(tlpconfig_defaults) == jsonconfigcount

    def test_tlp_version_1_1(self):
        version = "1_1"
        tlpconfig_defaults = extract_default_tlp_configs('../tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', '../tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        assert len(jsoncategories) == 11
        assert len(tlpconfig_defaults) == 91
        assert len(tlpconfig_defaults) == jsonconfigcount

    def test_tlp_version_1_2(self):
        version = "1_2"
        tlpconfig_defaults = extract_default_tlp_configs('../tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', '../tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        assert len(jsoncategories) == 11
        assert len(tlpconfig_defaults) == 100
        assert len(tlpconfig_defaults) == jsonconfigcount

    def test_tlp_version_1_3(self):
        version = "1_3"
        tlpconfig_defaults = extract_default_tlp_configs('../tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', '../tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        assert len(jsoncategories) == 11
        assert len(tlpconfig_defaults) == 99
        assert len(tlpconfig_defaults) == jsonconfigcount


if __name__ == '__main__':
    unittest.main()

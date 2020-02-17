import unittest
from importlib import reload

import os
os.environ['XDG_CONFIG_HOME'] = os.path.dirname(os.path.abspath(__file__)) + '/settings/default'
from tlpui import settings
from tlpui.file import read_default_tlp_file_config, get_json_schema_object_from_file


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
        reload(settings)
        version = "0_8"
        read_default_tlp_file_config('tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(jsoncategories), 11)
        self.assertEqual(80, len(settings.tlpconfig_defaults))
        self.assertEqual(jsonconfigcount, len(settings.tlpconfig_defaults))

    def test_tlp_version_0_9(self):
        reload(settings)
        version = "0_9"
        read_default_tlp_file_config('tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(jsoncategories), 11)
        self.assertEqual(84, len(settings.tlpconfig_defaults))
        self.assertEqual(jsonconfigcount, len(settings.tlpconfig_defaults))

    def test_tlp_version_1_0(self):
        reload(settings)
        version = "1_0"
        read_default_tlp_file_config('tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(jsoncategories), 11)
        self.assertEqual(90, len(settings.tlpconfig_defaults))
        self.assertEqual(jsonconfigcount, len(settings.tlpconfig_defaults))

    def test_tlp_version_1_1(self):
        reload(settings)
        version = "1_1"
        read_default_tlp_file_config('tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(jsoncategories), 11)
        self.assertEqual(91, len(settings.tlpconfig_defaults))
        self.assertEqual(jsonconfigcount, len(settings.tlpconfig_defaults))

    def test_tlp_version_1_2(self):
        reload(settings)
        version = "1_2"
        read_default_tlp_file_config('tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(jsoncategories), 11)
        self.assertEqual(100, len(settings.tlpconfig_defaults))
        self.assertEqual(jsonconfigcount, len(settings.tlpconfig_defaults))

    def test_tlp_version_1_3(self):
        reload(settings)
        version = "1_3"
        read_default_tlp_file_config('tlpui/defaults/tlp-{}.conf'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'tlpui/configschema/{}.json'.format(version))
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(jsoncategories), 11)
        self.assertEqual(99, len(settings.tlpconfig_defaults))
        self.assertEqual(jsonconfigcount, len(settings.tlpconfig_defaults))


if __name__ == '__main__':
    unittest.main()

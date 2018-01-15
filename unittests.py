import unittest
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import mainui
from configui import get_tlp_categories
from file import read_tlp_file_config, get_json_schema_object_from_file


def get_config_count(categories):
    configcount = 0
    for category in categories:
        configs = category['configs']
        for config in configs:
            if 'group' in config:
                groupitems = config['ids']
                configcount += len(groupitems)
            else:
                configcount += 1;
    return configcount


class MyTestCase(unittest.TestCase):
    def test_tlp_version_0_8(self):
        version = "0_8"
        tlpconfig = read_tlp_file_config('unittests/tlp-config-{}'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'configschema/{}.json'.format(version))

        configfilecategories = get_tlp_categories(Gtk.Window(), jsoncategories)
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(configfilecategories), 11)
        self.assertEqual(80, len(tlpconfig))
        self.assertEqual(jsonconfigcount, len(tlpconfig))

    def test_tlp_version_0_9(self):
        version = "0_9"
        tlpconfig = read_tlp_file_config('unittests/tlp-config-{}'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'configschema/{}.json'.format(version))

        configfilecategories = get_tlp_categories(Gtk.Window(), jsoncategories)
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(configfilecategories), 11)
        self.assertEqual(84, len(tlpconfig))
        self.assertEqual(jsonconfigcount, len(tlpconfig))

    def test_tlp_version_1_0(self):
        version = "1_0"
        tlpconfig = read_tlp_file_config('unittests/tlp-config-{}'.format(version))
        jsoncategories = get_json_schema_object_from_file('categories', 'configschema/{}.json'.format(version))

        configfilecategories = get_tlp_categories(Gtk.Window(), jsoncategories)
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(configfilecategories), 11)
        self.assertEqual(90, len(tlpconfig))
        self.assertEqual(jsonconfigcount, len(tlpconfig))


if __name__ == '__main__':
    unittest.main()

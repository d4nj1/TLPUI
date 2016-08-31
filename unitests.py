import unittest
from json import load

from configui import get_tlp_categories
from file import read_tlp_file_config, get_json_schema_object_from_file


def get_config_count(categories):
    configcount = 0
    for category in categories:
        configs = category['configs']
        configcount += len(configs);
    return configcount


class MyTestCase(unittest.TestCase):
    def test_config_categories(self):
        configfilelist = read_tlp_file_config("/etc/default/tlp")
        configfilecategories = get_tlp_categories(configfilelist)

        self.assertEqual(len(configfilecategories), 12)

    def test_tlp_file_vs_json_config(self):
        # tlp file config
        configfilelist = read_tlp_file_config("/etc/default/tlp")

        # json config
        jsoncategories = get_json_schema_object_from_file('categories', 'configschema.json')
        jsonconfigcount = get_config_count(jsoncategories)

        self.assertEqual(len(configfilelist), 80)
        self.assertEqual(len(configfilelist), jsonconfigcount)


if __name__ == '__main__':
    unittest.main()

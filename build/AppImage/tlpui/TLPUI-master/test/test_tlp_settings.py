import unittest
import linecache
import shutil

import os
os.environ['XDG_CONFIG_HOME'] = os.path.dirname(os.path.abspath(__file__)) + '/settings/default'
from tlpui import settingshelper


class MyTestCase(unittest.TestCase):

    def test_tlp_settings_broken(self):
        os.environ['XDG_CONFIG_HOME'] = os.path.dirname(os.path.abspath(__file__)) + '/settings/default'
        userconfig = settingshelper.UserConfig()
        userconfig.userconfigfile.write_text("[default]")
        userconfig.read_user_config()
        assert linecache.getline(str(userconfig.userconfigfile), 1) == "[default]\n"
        assert linecache.getline(str(userconfig.userconfigfile), 2) == "language = en_EN\n"
        assert linecache.getline(str(userconfig.userconfigfile), 3) == "activeoption = 0\n"
        assert linecache.getline(str(userconfig.userconfigfile), 4) == "activecategory = 0\n"
        assert linecache.getline(str(userconfig.userconfigfile), 5) == "windowxsize = 900\n"
        assert linecache.getline(str(userconfig.userconfigfile), 6) == "windowysize = 600\n"

    def test_tlp_settings_creation(self):
        newsettingspath = os.path.dirname(os.path.abspath(__file__)) + '/settings/creation'
        os.environ['XDG_CONFIG_HOME'] = newsettingspath
        if os.path.exists(newsettingspath):
            shutil.rmtree(newsettingspath)
        userconfig = settingshelper.UserConfig()
        assert linecache.getline(str(userconfig.userconfigfile), 1) == "[default]\n"
        assert linecache.getline(str(userconfig.userconfigfile), 2) == "language = en_EN\n"
        assert linecache.getline(str(userconfig.userconfigfile), 3) == "activeoption = 0\n"
        assert linecache.getline(str(userconfig.userconfigfile), 4) == "activecategory = 0\n"
        assert linecache.getline(str(userconfig.userconfigfile), 5) == "windowxsize = 900\n"
        assert linecache.getline(str(userconfig.userconfigfile), 6) == "windowysize = 600\n"


if __name__ == '__main__':
    unittest.main()

import unittest
import linecache
import shutil
from importlib import reload

import os
os.environ['XDG_CONFIG_HOME'] = os.path.dirname(os.path.abspath(__file__)) + '/settings/default'
from tlpui import settings


class MyTestCase(unittest.TestCase):
    def test_tlp_settings_broken(self):
        os.environ['XDG_CONFIG_HOME'] = os.path.dirname(os.path.abspath(__file__)) + '/settings/default'
        reload(settings)
        settings.userconfigfile.write_text("[default]")
        reload(settings)
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 1), "[default]\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 2), "language = en_EN\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 3), "tlpconfigfile = /etc/default/tlp\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 4), "activecategorie = 0\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 5), "windowxsize = 900\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 6), "windowysize = 600\n")


    def test_tlp_settings_creation(self):
        newsettingspath = os.path.dirname(os.path.abspath(__file__)) + '/settings/creation'
        os.environ['XDG_CONFIG_HOME'] = newsettingspath
        if os.path.exists(newsettingspath):
            shutil.rmtree(newsettingspath)
        reload(settings)
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 1), "[default]\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 2), "language = en_EN\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 3), "tlpconfigfile = /etc/default/tlp\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 4), "activecategorie = 0\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 5), "windowxsize = 900\n")
        self.assertEqual(linecache.getline(str(settings.userconfigfile), 6), "windowysize = 600\n")


if __name__ == '__main__':
    unittest.main()

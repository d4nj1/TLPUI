from io import open
import os
from json import load


lastvalue = ''
custom_translations = {
    'TLP_PERSISTENT_DEFAULT':       ['1_0', '1_1'],         # ID  / since 1.0
    'CPU_SCALING_GOVERNOR':         ['all'],                # GRP
    'CPU_SCALING_FREQ':             ['all'],                # GRP
    'CPU_HWP':                      ['1_0', '1_1'],         # GRP / since 1.0
    'ENERGY_PERF_POLICY':           ['all'],                # GRP
    'DISK_APM_LEVEL':               ['all'],                # GRP
    'DISK_IOSCHED':                 ['all'],                # ID
    'SATA_LINKPWR':                 ['all'],                # GRP
    'SATA_LINKPWR_BLACKLIST':       ['0_9', '1_0', '1_1'],  # ID  / since 0.9
    'AHCI_RUNTIME_PM':              ['0_9', '1_0', '1_1'],  # GRP / since 0.9
    'AHCI_RUNTIME_PM_TIMEOUT':      ['0_9', '1_0', '1_1'],  # ID  / since 0.9
    'WIFI_PWR':                     ['all'],                # GRP
    'BAY_POWEROFF':                 ['1_0', '1_1'],         # GRP / since 1.0
    'BAY_POWEROFF_ON_BAT':          ['0_8', '0_9'],         # ID  / until 0.9
    'RUNTIME_PM_ALL':               ['0_8', '0_9'],         # ID  / until 0.9
    'RUNTIME_PM_DRIVER_BLACKLIST':  ['all'],                # ID
    'USB_BLACKLIST_BTUSB':          ['1_0', '1_1'],         # ID  / since 1.0
    'USB_BLACKLIST_PHONE':          ['1_0', '1_1'],         # ID  / since 1.0
    'USB_BLACKLIST_PRINTER':        ['1_1'],                # ID  / since 1.1
    'USB_BLACKLIST_WWAN':           ['all'],                # ID
    'RESTORE_THRESHOLDS_ON_BAT':    ['1_0', '1_1']          # ID  / since 1.0
}


def get_json_schema_object_from_file(objectname: str, filename: str) -> dict:
    jsonfile = open(filename)
    jsonobject = load(jsonfile)
    jsonfile.close()
    return jsonobject[objectname]


def add_to_list(listobject: list, value: str):
    global lastvalue
    if not value in listobject:
        if lastvalue in listobject:
            lastindex = listobject.index(lastvalue)
            listobject.insert(lastindex+1, value)
        else:
            listobject.append(value)

    lastvalue = value


def create_translateable_strings_header_file():
    """ This method extracts items for translation from configschema.json and puts them in new file with
    header extension (.h) because poedit and other po-tools do not support JSON files right now. This method
    should be called any time configschema.json changes and translation needs to be updated.
    Change configschema.json -> run this script -> update po files from source with utility (e.g. poedit)"""

    translateobjects = list()

    for file in os.listdir('../configschema'):
        if not file.endswith('.json'):
            continue

        configversion = file.replace('.json', '')
        versionfile = open('configschema.{}.json.h'.format(configversion), 'w+')

        categories = get_json_schema_object_from_file('categories', '../configschema/' + file)
        for category in categories:
            add_to_list(translateobjects, category['name'] + '__CATEGORY_TITLE')
            configs = category['configs']
            for config in configs:
                if 'group' in config:
                    if config['group'] in custom_translations.keys() \
                            and any(v in custom_translations.get(config['group']) for v in {configversion, 'all'}):
                        # versionfile.write('_(\"' + config['group'] + '__GROUP_TITLE' + '\");\n')
                        versionfile.write('_(\"' + config['group'] + '__GROUP_DESCRIPTION' + '\");\n')
                        # configitems = config['ids']
                        # for configitem in configitems:
                        #     versionfile.write('_(\"' + configitem['id'] + '__ID_TITLE' + '\");\n')
                    elif config['group'] not in custom_translations.keys():
                        # add_to_list(translateobjects, config['group'] + '__GROUP_TITLE')
                        add_to_list(translateobjects, config['group'] + '__GROUP_DESCRIPTION')
                        # configitems = config['ids']
                        # for configitem in configitems:
                        #     add_to_list(translateobjects, configitem['id'] + '__ID_TITLE')
                else:
                    if config['id'] in custom_translations.keys() \
                            and any(v in custom_translations.get(config['id']) for v in {configversion, 'all'}):
                        # versionfile.write('_(\"' + config['id'] + '__ID_TITLE' + '\");\n')
                        versionfile.write('_(\"' + config['id'] + '__ID_DESCRIPTION' + '\");\n')
                    elif config['id'] not in custom_translations.keys():
                        # add_to_list(translateobjects, config['id'] + '__ID_TITLE')
                        add_to_list(translateobjects, config['id'] + '__ID_DESCRIPTION')

        versionfile.close()

    newfile = open('configschema.json.h', 'w+')
    for item in translateobjects:
        newfile.write('_(\"' + item + '\");\n')
    newfile.close()


create_translateable_strings_header_file()

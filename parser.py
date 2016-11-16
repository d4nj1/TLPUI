import argparse
import configparser
from lang import available_locales

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lang', help='language in iso format')

args = parser.parse_args()
lang = available_locales.get(args.lang)

config = configparser.ConfigParser()
config.read('app.ini')
try:
    if lang == '' or lang == None:
        lang = config['locale']['lang']
    elif lang == config['locale']['lang']:
        pass
    else:
        config['locale']['lang'] = lang
        with open('app.ini', 'w') as configfile:
            config.write(configfile)
except ValueError as e:
    print(e)
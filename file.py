import re
from os import remove, close
from shutil import move
from tempfile import mkstemp

from config import TlpConfig


def read_tlp_file_config(filename) -> list:
    propertypattern = re.compile('^#?[A-Z_\d]+=')
    fileproperties = list()
    fileopener = open(filename)
    lines = fileopener.readlines()
    fileopener.close()
    linenumber = 0

    for line in lines:
        linenumber += 1
        if propertypattern.match(line):
            cleanline = line.lstrip().rstrip()

            if (cleanline.startswith('#')):
                enabled = False
                cleanline = cleanline.lstrip('#')
            else:
                enabled = True

            property = cleanline.split('=', maxsplit=1)
            propertyname = property[0]
            propertyvalue = property[1]

            if propertyvalue.startswith('\"') and propertyvalue.endswith('\"'):
                isquoted = True
                propertyvalue = propertyvalue.lstrip('\"').rstrip('\"')
            else:
                isquoted = False

            fileproperties.append(TlpConfig(line, linenumber, enabled, propertyname, propertyvalue, isquoted))

    return fileproperties


def write_tlp_file_config(changedproperties, filename):
    fh, tmpfilename = mkstemp()
    newfile = open(tmpfilename, 'w')

    oldfile = open(filename)
    lines = oldfile.readlines()
    oldfile.close()

    linenumber = 0

    for line in lines:
        linenumber += 1
        changedline = False

        for property in changedproperties:
            if line == property[0] and linenumber == property[1]:
                newfile.write(property[2] + '\n')
                changedline = True
                break

        if not changedline:
            newfile.write(line)

    newfile.close()
    close(fh)
    oldfile.close()

    remove(filename)
    move(tmpfilename, filename)

    # print('Config file written.')
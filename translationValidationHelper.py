#!/usr/bin/env python3

import sys
import gettext
import difflib
from pathlib import Path
from tlpui import settings
from googletrans import Translator


def validate_translation(trans: Translator, check_locale: str, language_file: str):
    main_lang = "en"
    main_locale = "en_EN"
    main_translation_catalog = gettext.translation(domain=language_file, localedir=settings.langdir, languages=[main_locale])._catalog
    check_translation_catalog = gettext.translation(domain=language_file, localedir=settings.langdir, languages=[check_locale])._catalog

    differ = difflib.HtmlDiff()
    charset = 'utf-8'
    unknown_items = []
    html = f"Checking locale <b>{check_locale}</b> for <b>{language_file}</b></br></br>"

    for item in main_translation_catalog:
        if item == '' or '__ID_TITLE' in item or '__GROUP_TITLE' in item:
            continue
        if item not in check_translation_catalog:
            unknown_items.append(item)
            continue
        if '_DESCRIPTION' in item or '_TITLE' in item:
            html += f"</br><h3>{item}</h3></br>"

        check_item = check_translation_catalog[item]
        translated_item = trans.translate(check_item, dest=main_lang).text

        html += f"{check_item}</br>"
        html += differ.make_table([translated_item], [main_translation_catalog[item]])
        html += "</br>"

    if len(unknown_items) > 0:
        print('Translations missing for:')
        print(unknown_items)

    html_output = (differ._file_template % dict(
            styles=differ._styles,
            legend=differ._legend,
            table=html,
            charset=charset
        )).encode(charset, 'xmlcharrefreplace').decode(charset)

    html_file = open(f"diffresult-{check_locale}-{language_file}.html", "w")
    html_file.write(html_output)
    html_file.close()


if len(sys.argv) < 2:
    print('No locale provided. Must be in format like xx_XX')
    sys.exit()

locale = sys.argv[1]
locale_path = Path(f"{settings.langdir}{locale}")
if not locale_path.exists() and not locale_path.is_dir():
    print(f"Locale folder '{locale_path}' does not exist")
    sys.exit()

print(f"Evaluating locale: {locale}")
translator = Translator()
validate_translation(translator, locale, 'configdescriptions')
validate_translation(translator, locale, 'mainui')
validate_translation(translator, locale, 'statui')
validate_translation(translator, locale, 'uihelper')

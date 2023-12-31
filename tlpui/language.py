"""Provide translation."""

from . import settings
import gettext


def load_lang(langfile):
    """Load language from file."""
    translation = gettext.translation(langfile, settings.langdir, [settings.userconfig.language])

    versionlangfile = f"{langfile}{settings.tlpbaseversion}"
    if gettext.find(versionlangfile, settings.langdir, [settings.userconfig.language]) is None:
        return translation.gettext

    versiontranslation = gettext.translation(versionlangfile, settings.langdir, [settings.userconfig.language])
    versiontranslation.add_fallback(translation)
    return versiontranslation.gettext


CDT_ = load_lang('configdescriptions')
MT_ = load_lang('mainui')
ST_ = load_lang('statui')
UH_ = load_lang('uihelper')

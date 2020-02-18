from . import settings
import gettext


def load_lang(langfile):
    translation = gettext.translation(domain=langfile, localedir=settings.langdir, languages=[settings.language])

    versionlangfile = "{}{}".format(langfile, settings.tlpbaseversion)
    if gettext.find(domain=versionlangfile, localedir=settings.langdir, languages=[settings.language]) is None:
        return translation.gettext
    else:
        versiontranslation = gettext.translation(domain=versionlangfile, localedir=settings.langdir, languages=[settings.language])
        versiontranslation.add_fallback(translation)
        return versiontranslation.gettext


CDT_ = load_lang('configdescriptions')
MT_ = load_lang('mainui')
ST_ = load_lang('statui')
UH_ = load_lang('uihelper')

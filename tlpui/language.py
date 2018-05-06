from . import settings
import gettext


def load_lang(translation):
    translation = gettext.translation(translation, settings.langdir, languages=[settings.language])
    return translation.gettext


CDT_ = load_lang('configdescriptions')
MT_ = load_lang('mainui')
ST_ = load_lang('statui')
UH_ = load_lang('uihelper')

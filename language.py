import settings
import gettext


def load_lang(translation):
    translation = gettext.translation(translation, settings.langdir, languages=[settings.language])
    return translation.gettext


MT_ = load_lang('mainui')
CT_ = load_lang('configui')
CDT_ = load_lang('configdescriptions')
ST_ = load_lang('statui')

from setuptools import setup
from tlpui import __version__

setup(
    name="TLPUI",
    version=__version__,
    author="Daniel Christophis",
    author_email="code@devmind.org",
    description="GTK UI for tlp (Python 3)",
    url="https://github.com/d4nj1/TLPUI",
    license="GPLv2",
    packages=["tlpui", "tlpui.ui_config_objects"],
    package_data={'tlpui': [
        'styles.css',
        'configschema/*.json',
        'defaults/*.conf',
        'icons/*.svg',
        'icons/flags/*.png',
        'icons/themeable/hicolor/scalable/actions/*.svg',
        'icons/themeable/hicolor/scalable/apps/*.svg',
        'lang/*/LC_MESSAGES/*.mo'
    ]},
    entry_points={
        'gui_scripts': [
            'tlpui = tlpui.__main__:main'
        ]
    },
    data_files=[
        ('/usr/share/applications', ["tlpui.desktop"])
    ]
)

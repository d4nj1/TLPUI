from setuptools import setup

setup(
    name="TLPUI",
    version="1.3.1",
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
        'icons/themeable/hicolor/scalable/actions/*.svg',
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

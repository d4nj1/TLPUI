from setuptools import setup

setup(
    name="TLPUI",
    version="0.1",
    author="Daniel Christophis",
    author_email="code@devmind.org",
    description="GTK UI for tlp (Python 3)",
    url="https://github.com/d4nj1/TLPUI",
    license="GPLv2",
    packages=["tlpui", "tlpui.ui_config_objects"],
    package_data={'tlpui': [
        'styles.css',
        'configschema/*.json',
        'icons/*.svg',
        'icons/themeable/hicolor/scalable/actions/*.svg',
        'lang/*/LC_MESSAGES/*.mo'
    ]},
    entry_points={
        'gui_scripts': [
            'tlpui = tlpui.__main__:main'
        ]
    }
)

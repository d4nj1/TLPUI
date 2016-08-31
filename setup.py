from setuptools import setup

setup(
    name="TLPUI",
    version="0.1",
    author="Daniel Christophis",
    author_email="code@devmind.org",
    py_modules=["ui_config_objects"],
    scripts=["config.py", "configui.py", "css.py", "file.py", "mainui.py", "statui.py", "tlpui.py"]
)
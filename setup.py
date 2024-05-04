from setuptools import setup, find_packages
import gmo_fx

DESCRIPTION = "GMO社のFX API用Pythonライブラリ"
NAME = "gmo_fx"
AUTHOR = "Rikito Noto"
AUTHOR_EMAIL = "rikitonoto@gmail.com"
URL = "https://github.com/RikitoNoto/gmo-fx-py"
LICENSE = "MIT"
DOWNLOAD_URL = "https://github.com/RikitoNoto/gmo-fx-py"
VERSION = gmo_fx.__version__
INSTALL_REQUIRES = [
    "requests>=2.31.0",
]
PACKAGES = [
    "gmo_fx",
]

with open("README.md", "r") as fp:
    readme = fp.read()

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=readme,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    download_url=DOWNLOAD_URL,
    version=VERSION,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
)

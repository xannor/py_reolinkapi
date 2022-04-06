""" setup """

from distutils.core import setup
from setuptools import find_packages


setup(
    name="reolinkapi",
    packages=find_packages(where="reolinkapi"),
    package_dir={"": "reolinkapi"},
    version="0.0.1",
    license="MIT",
    description="Reolink camera api for python",
    author="xannor",
    author_email="",
    url="https://github.com/xannor/reolinkapipy",
    download_url="https://github.com/xannor/reolinkapipy/releases/latest",
    keywords=["Reolink"],
    install_requires=["aiohttp"],
    classifiers=[
        "Development Status :: 5 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)

#!/usr/bin/env python
from pathlib import Path

from setuptools import setup

readme = Path("README.rst").read_text(encoding="utf-8")
history = Path("CHANGES.rst").read_text(encoding="utf-8")


setup(
    name="html_text",
    version="0.7.0",
    description="Extract text from HTML",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    author="Konstantin Lopukhin",
    author_email="kostia.lopuhin@gmail.com",
    url="https://github.com/zytedata/html-text",
    packages=["html_text"],
    package_data={
        "html_text": ["py.typed"],
    },
    include_package_data=True,
    install_requires=[
        "lxml",
        "lxml-html-clean",
    ],
    license="MIT license",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)

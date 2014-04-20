#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name="tornadoflowdock",
    version="0.0.1",
    description="Integrates Flowdock with Tornado",
    author="Thomas Rabaix",
    author_email="thomas.rabaix@gmail.com",
    url="https://github.com/rande/tornado-flowdock",
    packages = find_packages(),
    install_requires=[],
    include_package_data = True,
)

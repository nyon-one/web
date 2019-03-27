#!/usr/bin/env python

from distutils.core import setup

setup(name='www',
      version='1.2.4',
      description='Utilities for Requests module',
      author='nyon.one',
      install_requires=['requests-html'],
      packages=['www'],
     )

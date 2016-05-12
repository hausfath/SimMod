#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('beam_carbon/beam.py').read(),
    re.M
    ).group(1)
 
with open('README.md', 'rb') as f:
    long_description = f.read().decode('utf-8')
 
setup(
    name='beam_carbon',
    packages=['beam_carbon'],
    entry_points={
        'console_scripts': ['beam_carbon = beam_carbon.beam:main']
    },
    license='GPLv3',
    version=version,
    description='Python command line application for running the BEAM carbon cycle.',
    long_description=long_description,
    author='Nathan Matteson',
    author_email='matteson@obstructures.org',
    url='',
    cmdclass={'build_ext': build_ext},
    setup_requires=['numpy'],
)
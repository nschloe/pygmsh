# -*- coding: utf-8 -*-
#
import os
from distutils.core import setup
import codecs

from pygmsh import __name__, __version__, __author__, __author_email__


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except Exception:
        content = ''
    return content

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    packages=['pygmsh'],
    description='Python frontend for Gmsh',
    long_description=read('README.rst'),
    url='https://github.com/nschloe/pygmsh',
    download_url='https://pypi.python.org/pypi/pygmsh',
    license='License :: OSI Approved :: MIT License',
    platforms='any',
    requires=[
        'numpy'
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics'
        ]
    )

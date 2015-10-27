# -*- coding: utf-8 -*-
import os
from distutils.core import setup
import codecs

from pygmsh import __name__, __version__, __author__, __author_email__

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname),
                       encoding='utf-8'
                       ).read()

setup(name=__name__,
      packages=['pygmsh'],
      version=__version__,
      description='Python frontend for Gmsh',
      long_description=read('README.md'),
      author=__author__,
      author_email=__author_email__,
      url='https://github.com/nschloe/pygmsh/',
      license='License :: OSI Approved :: MIT License',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Mathematics'
          ],
      )

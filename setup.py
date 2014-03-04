# -*- coding: utf-8 -*-
import os
from distutils.core import setup
import codecs


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname),
                       encoding='utf-8'
                       ).read()

setup(name='python4gmsh',
      packages=['python4gmsh'],
      version='0.1.0',
      description='Python frontend for Gmsh',
      long_description=read('README.md'),
      author='Nico Schlömer',
      author_email='nico.schloemer@gmail.com',
      url='https://github.com/nschloe/python4gmsh/',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Mathematics'
          ],
      )

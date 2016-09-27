# -*- coding: utf-8 -*-

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(name='biogridpy',
	  version='0.1',
	  description='Python client for the BioGRID REST API webservice',
	  license='MIT',
	  keywords=['genetics', 'genomics', 'interaction', 'bioinformatics'],
	  classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Bio-Informatics'],
	  author='Kevin Arvai',
	  author_email='arvkevi@gmail.com',
	  download_url = 'https://github.com/arvkevi/biogridpy/tarball/0.1',
	  url = 'https://github.com/arvkevi/biogridpy',
	  packages=['biogridpy'],
zip_safe=False)
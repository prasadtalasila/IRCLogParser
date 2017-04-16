from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command import easy_install
from os import path
from codecs import open
import pip

try:
	import numpy
except ImportError:
	pip.main(['install', 'numpy'])

try:
	import scipy
except ImportError:
	pip.main(['install', 'scipy'])


current_path = path.abspath(path.dirname(__file__))

with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='IRCLogParser',
    version='1.0.0',
    description='A Parser for IRC chat Logs',
    long_description=long_description,
    url='https://github.com/prasadtalasila/IRCLogParser',
    author='Prasad Talasila',
    author_email='tsrkp@goa.bits-pilani.ac.in',
    license='MIT',

    classifiers=[
        'Development Status :: Released v1.0.0',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Topic :: Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='IRC parser data-analysis research development',
    packages=find_packages(exclude=['docs', 'tests']),

    dependency_links = ['https://github.com/rtfd/sphinx_rtd_theme/archive/0.2.4.tar.gz#egg=sphinx_rtd_theme-0.2.4'],

	setup_requires = [
        'graphviz'],

    install_requires = [
        'networkx',
        'matplotlib',
        'graphviz',
        'pygraphviz',
        'scikit-learn',
        'pandas',
        'python-igraph',
        'sphinx',
        'pyyaml',
        'sphinx_rtd_theme>=0.2.4',
        't3fieldlisttable',
        't3tablerows',
        't3targets',
        'sphinxcontrib-googlechart',
        'sphinxcontrib-googlemaps',
        'sphinxcontrib-httpdomain',
        'sphinxcontrib-slide',
        'sphinxcontrib.youtube',
        'nltk',
        'plotly',
        'ddt'
    ],
)

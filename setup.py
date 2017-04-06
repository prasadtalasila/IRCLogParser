from setuptools import setup, find_packages
from os import path
from codecs import open
import numpy
import scipy

current_path = path.abspath(path.dirname(__file__))

with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='IRCLogParser',
    version='1.0.0',
    description='A Parser for IRC chat Logs',
    long_description=long_description,
    url='https://github.com/prasadtalasila/IRCLogParser',
    download_url='https://github.com/prasadtalasila/IRCLogParser/archive/v1.0.0.tar.gz',
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
    packages=['IRCLogParser'],

    install_requires=[
        'scipy',
        'numpy',
        'networkx',
        'matplotlib',
        'pygraphviz',
        'scikit-learn',
        'pandas',
        'python-igraph',
        'sphinx',
        'pyyaml',
        't3SphinxThemeRtd',
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

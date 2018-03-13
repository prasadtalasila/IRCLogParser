from setuptools import setup, find_packages
from os import path
from codecs import open
import pip

current_path = path.abspath(path.dirname(__file__))

#install numpy and scipy if not exists seperately since compiled header are required
try:
	import numpy
except ImportError:
	pip.main(['install','numpy'])

try:
	import scipy
except ImportError:
	pip.main(['install','scipy'])

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='IRCLogParser',
    version='1.0.0',
    description='A Parser for IRC chat Logs',
    long_description=long_description,
    url='https://github.com/prasadtalasila/IRCLogParser',
    author='Prasad Talasila',
    author_email='tsrkp@goa.bits-pilani.ac.in',
    download_url='https://github.com/prasadtalasila/IRCLogParser/archive/v1.0.0.tar.gz',
    license='MIT',
    include_package_data=True,
    keywords='IRC parser data-analysis research development',
    packages=find_packages(exclude=['docs', 'tests']),
    
    setup_requires=[
    	'graphviz'
    ],

    install_requires=[
        'networkx==1.11',
        'matplotlib',
        'pygraphviz',
        'scikit-learn',
        'pandas',
        'python-igraph',
        'nltk',
        'plotly==2.4.1',
        'ddt',
        'mock'
        
    ],
    extra_requires={
    	'dev': [
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
        	'codeclimate-test-reporter',
        	'memory_profiler',
        	'snakefood'
    	]
    }
        
)

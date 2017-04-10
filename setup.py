from setuptools import setup, find_packages
from os import path
from codecs import open

current_path = path.abspath(path.dirname(__file__))

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
        'ddt',
        'codeclimate-test-reporter',
        'memory_profiler',
        'snakefood'
    ],
)

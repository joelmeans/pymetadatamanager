__author__="jlmeans"
__date__ ="$Jan 19, 2010 12:37:38 PM$"

from setuptools import setup,find_packages

setup (
  name = 'pymetadatamanager',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'Joel Means',
  author_email = 'means.joel@gmail.com',

  summary = 'A metadatamanager for video files',
  url = 'http://github.com/joelmeans/pymetadatamanager',
  license = '',
  long_description= 'This program will scan directories for video files and lookup metadata information from themoviedb.com and thetvdb.org.  It will write out xbmc-compatible nfo files and save artwork.  It is a very rough work in progress.',

  # could also include long_description, download_url, classifiers, etc.

  
)

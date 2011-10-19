#!/usr/bin/env python

__author__="jlmeans"
__date__ ="$Jan 19, 2010 12:37:38 PM$"

from distutils.core import setup

setup (
  name = 'pymetadatamanager',
  version = '0.1',
  description = 'A metadatamanager for video files',
  author = 'Joel Means',
  author_email = 'means.joel@gmail.com',
  url = 'http://github.com/joelmeans/pymetadatamanager',
  packages = ['pymetadatamanager'],
  provides = ['pymetadatamanager'],
  requires = ['PyQt4'],
  scripts = ['metadatamanager'],
  license = 'GPLv2',
  long_description= 'This program will scan directories for video files and lookup metadata information from themoviedb.com and thetvdb.org.  It will write out xbmc-compatible nfo files and save artwork.  It is a very rough work in progress.'
)

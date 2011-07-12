pymetadatamanager
====================

(c) 2009 - 2011 Joel Means <means.joel@gmail.com>.

For the latest version, please visit:
[http://github.com/joelmeans/pymediamanager](http://github.com/joel.means/pymediamanager)

## About the program 

This program is currently very rough.  The initial development has two purposes.  I wanted to learn python and I wanted a metadata manager that would work with thetvdb.org and themoviedatabase.com under Linux.  So I thought that I would learn python while writing the metadatamanager.  Since it is a learning tool and I don't have a ton of time to devote to it, don't expect a polished program for a while.  Any python programmers who want to help contribute, drop me an e-mail, fork it, and let's go.

## What currently works

As of now, there is a scraper

	scraper.py

which will prompt you for a directory of files to scrape and do a lookup on thetvdb.com.  It expects filenames of the form Show_Title_SSxEE.ext.  It grabs a list of matches to "Show_Title" and asks you which one is correct.  It then populates a database, TV.db, with the episodes found.

There is also a GUI for viewing and limited modification of what is in the database.  That is run as

	testing.py

This is written in PyQt4, which I am also learning as I go.

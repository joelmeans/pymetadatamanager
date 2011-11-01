pymetadatamanager
====================

(c) 2009 - 2011 Joel Means

For the latest version, please visit:
[http://github.com/joelmeans/pymediamanager](http://github.com/joel.means/pymediamanager)

## About the program 

The initial development of this program had two purposes.  I wanted to learn python and I wanted a metadata manager that would work with thetvdb.org and themoviedatabase.com under Linux.  So I thought that I would learn python while writing the metadatamanager.  Since it is a learning tool and I don't have a ton of time to devote to it, don't expect a polished program for a while.  Any python programmers who want to help contribute, drop me an e-mail, fork it, and let's go.

This is written in PyQt4, which I am also learning as I go.

## What currently works

I now have a reasonably working GUI including menu options to scan, set the media directory and clear the cache.  There are also menu options to save the .nfo files and to save the selected artwork. You can use

	python setup.py build
	sudo python setup.py install

to install it and run

	pymetadatamanager

to run the program.  

## Updates

10/05/2011 - I have added the ability to scrape from the GUI (menu Tools/Scan Files).  The scraper.py script still works fine, but this is an important feature.  Also, I have renamed testing.py to main.py and reorganized the entire project.

10/26/2011 - The GUI is now functional for settings and scraping.  Also, the main executable is now 'pymetadatamanager' and there is a proper 'setup.py' to allow installation of the executable and the supporting libraries.

11/01/2011 - I have reworked the GUI to be much more useful (in my opinion) and added the ability to save selected artwork and .nfo files.  The program is now rather useful.

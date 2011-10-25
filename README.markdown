pymetadatamanager
====================

(c) 2009 - 2011 Joel Means

For the latest version, please visit:
[http://github.com/joelmeans/pymediamanager](http://github.com/joel.means/pymediamanager)

## About the program 

This program is currently very rough.  The initial development has two purposes.  I wanted to learn python and I wanted a metadata manager that would work with thetvdb.org and themoviedatabase.com under Linux.  So I thought that I would learn python while writing the metadatamanager.  Since it is a learning tool and I don't have a ton of time to devote to it, don't expect a polished program for a while.  Any python programmers who want to help contribute, drop me an e-mail, fork it, and let's go.

This is written in PyQt4, which I am also learning as I go.

## What currently works

<del>As of now, there is a scraper</del>

	scraper.py

<del>which will prompt you for a directory of files to scrape and do a lookup on thetvdb.com.  It expects filenames of the form Show_Title_SSxEE.ext.  It grabs a list of matches to "Show_Title" and asks you which one is correct.  It then populates a database, TV.db, with the episodes found.</del>

<del>There is also a GUI for viewing and limited modification of what is in the database.  That is run as</del>

	testing.py

I now have a reasonably working GUI including menu options to scan, set the media directory and clear the cache.  The scraper.py script still works, but is unnecessary.  I have also set up the code base in a better manner and added a working setup.py file.  You can now use

	python setup.py build
	sudo python setup.py install

to install it and run

	pymetadatamanager

to run the program.  The main thing that is not working (which makes the program rather useless as it is) is the ability to save the artwork and nfo files.  This will take a bit to add, and I will get to it when I can.  I also have some plans to rearrange the GUI a bit.

## Updates

10/05/2011 - I have added the ability to scrape from the GUI (menu Tools/Scan Files).  The scraper.py script still works fine, but this is an important feature.  Also, I have renamed testing.py to main.py and reorganized the entire project.

10/26/2011 - The GUI is now functional for settings and scraping.  Also, the main executable is now 'pymetadatamanager' and there is a proper 'setup.py' to allow installation of the executable and the supporting libraries.

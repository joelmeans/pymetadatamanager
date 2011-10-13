pymetadatamanager TODO list
===========================

## A Note

Development of this project is slow and there is a lot to do to make this a working program.  I am just adding things here as I think of them.

## General TODO

01. <del>Learn how to organize a proper python program.</del>

02. Add a "copying" file for GPL info.

03. Standardize the header placed in the files.

## Technical TODO

01. Add a settings file and GUI interface for the settings.

02. <del>Add a button to the GUI to scan the media collection.</del>

    a) <del>Put the button.</del>
 
    b) <del>Rewrite scraper to allow interaction with GUI.</del> 

    c) <del>Popup a window for possible series name matches.</del>

    d) <del>Add code for auto-selecting if there is a single match.</del>

03. Add more filename parsing options.

04. Switch all ElementTree stuff over to QtXml.

05. <del>Extract series info zip file directly (now possible in Python 2.6).</del>

06. <del>Move the cache to the user's home directory.</del>

    a) <del>Figure out where and how to put this in windows.</del>

07. Find a better way to display artwork.

08. Clear the cache on exiting (maybe not, just add GUI option to clear).

09. Add a way to save the nfo file.

10. Add a way to save selected artworks.

11. Fix sorting to ignore "A", "An", "The".

12. <del>Get os.path stuff straightened out for cross-platform compatibility.</del>

13. <del>Figure out urllib vs urllib2 (why am I using both in tvdb.py?).</del>

14. Add ability to get season and episode numbers given series and episode name.

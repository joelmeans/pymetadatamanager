pymetadatamanager TODO list
===========================

## A Note

Development of this project is slow and there is a lot to do to make this a working program.  I am just adding things here as I think of them.

## General TODO

01. <del>Learn how to organize a proper python program.</del>

02. <del>Add a "copying" file for GPL info.</del>

03. <del>Standardize the header placed in the files.</del>

04.  Learn how to use py2app to make a Mac app bundle.

05.  Learn how to use py2exe to make a Windows exe.

06.  Learn how to package a nice deb.

## Technical TODO

01. <del>Add a settings file and GUI interface for the settings.</del>

02. <del>Add a button to the GUI to scan the media collection.</del>

    a) <del>Put the button.</del>
 
    b) <del>Rewrite scraper to allow interaction with GUI.</del> 

    c) <del>Popup a window for possible series name matches.</del>

    d) <del>Add code for auto-selecting if there is a single match.</del>

03. <del>Add more filename parsing options.</del>

04. <del>Switch all ElementTree stuff over to QtXml.</del>

05. <del>Extract series info zip file directly (now possible in Python 2.6).</del>

06. <del>Move the cache to the user's home directory.</del>

    a) <del>Figure out where and how to put this in windows.</del>

07. <del>Find a better way to display artwork.</del>

08. <del>Clear the cache on exiting (maybe not, just add GUI option to clear).</del>

09. <del>Add a way to save the nfo file.</del>

10. <del>Add a way to save selected artworks.</del>

11. Fix sorting to ignore "A", "An", "The".

12. <del>Get os.path stuff straightened out for cross-platform compatibility.</del>

13. <del>Figure out urllib vs urllib2 (why am I using both in tvdb.py?).</del>

14. <del>Add ability to get season and episode numbers given series and episode name.</del>

15. <del>Fix filename parsing to ignore extra stuff in the name after or between '.'.</del>

16. <del>Fix problem with having an apostrope in a show name (e.g. "Blue's Clues").</del>

17. <del>Add fanart capability.</del>

18. Add the ability to add artwork from the local system, not just thetvdb.org.

19. Add hilighting of missing episodes in season info tab.

20. <del>Add the ability to load local .nfo files.</del>

21. <del>Add dialog about saving files (right now it just won't respond, but it doesn't let you know why).</del>

22. <del>Add logging capability.</del>

23. Add movie capability with themoviedb.com.

24. Show info for episodes listed in season info (maybe a popup).

25. <del>Add ability to reload info from TVDB.com when local is used.</del>

26. Add local .nfo scraping as optional default.

27. Drop automatic updating from TVDB.com and add a button to optionally do it.

28. Add a way to show unmatched files and add some info manually.

29. Figure out handling of dvdorder on a per-series basis.

## Bug Fixes

01. <del>Scale posters to correct width (it is cutting off if too wide).</del>

02. <del>Remove series if there are no episodes present.

03. Add popup for input of ID for unmatched series name.

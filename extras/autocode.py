#!/usr/bin/env python

import os
import sys
import MySQLdb
import subprocess
from pymetadatamanager.tvdb import TVDB

#set some environment info
db_host = "192.168.1.15"
db_user = "mythtv"
db_passwd = "mythtv"
db_name = "mythconverg"
output_dir = "/var/media/videos/rips"

mythtranscode = "/usr/bin/mythtranscode"
mythtranscode_opts = "-l -m -e ps"
mythtranscode_opts_parsed = mythtranscode_opts.split()
mythtranscode_command = [mythtranscode]
for arg in mythtranscode_opts_parsed:
    mythtranscode_command.append(arg)

hb = "/usr/bin/HandBrakeCLI"
hb_opts = "-e x264  -q 20.0 -r 29.97 --pfr -a 1,1 -E faac,copy:ac3 -B 160,160 -6 dpl2,auto -R Auto,Auto -D 0.0,0.0 -f mp4 -4 -X 1280 --loose-anamorphic -m"
hb_deint = "--deinterlace"
hb_opts_parsed = hb_opts.split()
hb_command = [hb]
for arg in hb_opts_parsed:
    hb_command.append(arg)

#parse up input filename
infile = sys.argv[1]
basename = os.path.basename(infile)
chanid = basename.split("_")[0]
starttime = basename.split("_")[1].rstrip(".mpg")

#some show name replacements
subs = {       'The Office': 'The Office (US)',
                   'Castle': 'Castle (2009)',
               'Parenthood': 'Parenthood (2010)',
        'Last Man Standing': 'Last Man Standing (2011)'}

#interlaced channels
interlaced_chanids = ['1041', '1051', '1131']

#setup connection to MythTV Database
conn = MySQLdb.connect (host = db_host, user = db_user, passwd = db_passwd, db = db_name)
sql = conn.cursor()

#setup connection to thetvdb.com database
TVDB = TVDB()

#find all shows that have a cutlist
#sql_query="SELECT title,subtitle,basename,chanid FROM recorded WHERE cutlist='1'"
#sql.execute(sql_query)
#reply = sql.fetchall()

#get episode info from the myth database
sql_query = "SELECT title,subtitle,cutlist FROM recorded WHERE basename='%s'" % (basename)

sql.execute(sql_query)
reply = sql.fetchall()

#determine the output name and do the conversion
episode = reply[0]
print episode
series_name = episode[0]
episode_name = episode[1]
cutlist = episode[2]

if cutlist:
    if series_name in subs: 
        series_name = subs[series_name]
    season_ep = TVDB.get_ssxee_by_seriesname_episodename(series_name, episode_name)
    ep = (basename, series_name, str(season_ep[0]).zfill(2), str(season_ep[1]).zfill(2))
    print ep
    outfile = os.path.join(output_dir, "%s %sx%s" % (ep[1], ep[2], ep[3]))
    mythtranscode_inout = ["-c", chanid, "-s", starttime, "-o", "%s.mpg" % outfile]
    for arg in mythtranscode_inout:
        mythtranscode_command.append(arg)
    if chanid in interlaced_chanids:
        hb_command.append(hb_deint)
    hb_inout = ["-i", "%s.mpg" % outfile, "-o", "%s.m4v" % outfile]
    for arg in hb_inout:
        hb_command.append(arg)
    print mythtranscode_command
    print hb_command
#    subprocess.Popen(mythtranscode_command, stderr=subprocess.STDOUT,\
#                     stdout=subprocess.PIPE).communicate()
#    subprocess.Popen(hb_command, stderr=subprocess.STDOUT,\
#                     stdout=subprocess.PIPE).communicate()
else:
    print "Cutlist doesn't exist for recording %s" % (basename)

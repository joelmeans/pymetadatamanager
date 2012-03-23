#!/usr/bin/env python

import os
import sys
import math
import MySQLdb
import subprocess
from pymetadatamanager.tvdb import TVDB

infile = sys.argv[1]

#set some environment info
db_host = "192.168.1.15"
db_user = "mythtv"
db_passwd = "mythtv"
db_name = "mythconverg"
#output_dir = "/var/media/videos/rips"
output_dir = "/home/jmeans/Videos"

mythtranscode = "/usr/bin/mythtranscode"
mythtranscode_opts = "--honorcutlist --mpeg2"
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

mp4box = "/usr/bin/MP4Box"
mp4box_opts = "-chaps"
mp4box_opts_parsed = mp4box_opts.split()
mp4box_command = [mp4box]
for arg in mp4box_opts_parsed:
    mp4box_command.append(arg)

#parse up input filename
basename = os.path.basename(infile)
chanid = basename.split("_")[0]
starttime = basename.split("_")[1].rstrip(".mpg")

mythcommflag = "/usr/bin/mythutil"
mythcommflag_opts = "-q --getcutlist --chanid " + chanid + " --starttime " + starttime
mythcommflag_opts_parsed = mythcommflag_opts.split()
mythcommflag_command = [mythcommflag]
for arg in mythcommflag_opts_parsed:
    mythcommflag_command.append(arg)

#some show name replacements
subs = {       'The Office': 'The Office (US)',
                   'Castle': 'Castle (2009)',
               'Parenthood': 'Parenthood (2010)',
                   'Touch' : 'Touch (2012)',
                 'Missing' : 'Missing (2012)',
        'Last Man Standing': 'Last Man Standing (2011)'}

#interlaced channels
interlaced_chanids = ['1041', '1051', '1131']

#setup connection to MythTV Database
conn = MySQLdb.connect (host = db_host, user = db_user, passwd = db_passwd, db = db_name)
sql = conn.cursor()

#setup connection to thetvdb.com database
TVDB = TVDB()

#get episode info from the myth database
sql_query = "SELECT title,subtitle,cutlist FROM recorded WHERE basename='%s'" % (basename)

sql.execute(sql_query)
reply = sql.fetchall()

#determine the output name and do the conversion
episode = reply[0]
series_name = episode[0]
episode_name = episode[1]
cutlist = episode[2]

if cutlist:
    if chanid in interlaced_chanids:
        fps = 30000./1001.
    else:
        fps = 60000./1001.
    chapters = [(0,0,0,0)]
    cuts = subprocess.Popen(mythcommflag_command, stderr=subprocess.STDOUT, \
                            stdout=subprocess.PIPE).communicate()
    cuts = cuts[0].split("Cutlist: ")[1].rstrip('\n').split('-')
    for section in cuts:
        if not section.find(',') == -1:
            start = section.split(',')[0]
            end = section.split(',')[1]
            frames = int(end) - int(start)
            time = frames / fps
            time = time + 0.001 * chapters[-1][3] + \
                                  chapters[-1][2] + \
                            60. * chapters[-1][1] + \
                      60. * 60. * chapters[-1][0]
            milliseconds = int(math.floor((time - math.floor(time)) * 1000))
            seconds = int(math.floor(time))
            minutes = int(math.floor(seconds / 60.))
            hours = int(math.floor(minutes / 60.))
            seconds = seconds - minutes * 60
            minutes = minutes - hours * 60
            chapters.append((hours,minutes,seconds,milliseconds))

    formatted_chapters = []
    for chapter in chapters[0:-1]:
        formatted_time = "%02d:%02d:%02d.%03d" % \
                        (chapter[0], chapter[1], chapter[2], chapter[3])
        formatted_chapters.append(formatted_time)

    if series_name in subs: 
        series_name = subs[series_name]
    season_ep = TVDB.get_season_episode_by_name(series_name, \
                                                         episode_name)
    ep = (basename, series_name, str(season_ep[0]).zfill(2), \
          str(season_ep[1]).zfill(2))
    output_name = "%s %sx%s" %(ep[1], ep[2], ep[3])
    outfile = os.path.join(output_dir, output_name)
    mythtranscode_inout = ["--chanid", chanid, "--starttime", starttime, \
                           "--outfile", "%s.mpg" % outfile]
    for arg in mythtranscode_inout:
        mythtranscode_command.append(arg)
    if chanid in interlaced_chanids:
        hb_command.append(hb_deint)
    hb_inout = ["-i", "%s.mpg" % outfile, "-o", "%s.m4v" % outfile]
    for arg in hb_inout:
        hb_command.append(arg)
    print "Transcoding %s.mpg." % (output_name,)
    subprocess.Popen(mythtranscode_command, stderr=subprocess.STDOUT,\
                     stdout=subprocess.PIPE).communicate()
    print "Converting %s.mpg to %s.m4v." % (output_name, output_name)
    subprocess.Popen(hb_command, stderr=subprocess.STDOUT,\
                     stdout=subprocess.PIPE).communicate()
    os.remove("%s.mpg" % (outfile,))
    os.remove("%s.mpg.map" % (outfile,))
    print "Writing chapter file %s.txt." % (output_name,)
    chap_file = open("%s.txt" % (outfile,), 'w')
    for i in range(0,len(formatted_chapters)):
        chap_file.write("%s Chapter %d\n" % (formatted_chapters[i], i + 1))
    chap_file.close()
#    mp4box_command.append("%s.txt" % (outfile,))
#    mp4box_command.append("%s.m4v" % (outfile,))
#    subprocess.Popen(mp4box_command, stderr=subprocess.STDOUT,\
#                     stdout=subprocess.PIPE).communicate()
#    os.remove("%s.txt" % (outfile,))
else:
    print "Cutlist doesn't exist for recording %s" % (basename)

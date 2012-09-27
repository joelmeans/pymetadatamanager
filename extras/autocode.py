#!/usr/bin/env python

########################################################################
#  autocode.py works with MythTV 0.25 or higher.  It takes in the
#  start time of a recording (in UTC, Iso format), the chanid of
#  the recording and the desired output format (mkv or m4v at this
#  time).  It will transcode the recording to remove commercials 
#  (requires a cutlist) using mythtranscode and the convert the 
#  video to x264 in the requested container using HandBrakeCLI.  It is
#  designed to work with MPEG2/AC3 recordings from an HDHomerun.
#  For mkv output, it will also attach the cover art from MythTV and 
#  write chapter markers at the commercial cuts (requires mkvmerge).
#  For m4v, it creates an aac audio track as the first track and then
#  copies over the original ac3 track.  It also copies a chapter mark
#  file and the artwork to the output directory.  These can then be
#  added to the m4v file using something like Subler on Mac OS X.
#  The recommended method for using it is as a user job in MythTV.
#  Set up the job with the desired name and use the following as the 
#  command:
#    <path>/autocode.py [-lnc] [-f m4v] %STARTTIMEISOUTC% %CHANID%
#  Be sure to set the ip/port of the mythtv services api below as
#  well as the desired output directory and temp directory.
#  Note that you need to copy 45-autocode.py to /etc/rsyslog.d and setup
#  the appropriate logging directory (if you use syslog for mythtv
#  logging, this is already done).
########################################################################

import os
import sys
import math
import subprocess
import argparse
import urllib
import urllib2
import Image
import StringIO
import re
import tempfile
import shutil
import logging
from logging.handlers import SysLogHandler
from PyQt4 import QtXml

#set some environment info
services_ip = '192.168.1.15'
services_port = '6544'
output_dir = '/var/media/videos/rips'
tempdir = '/tmp'      # Where to create the temporary directory

#some show name replacements
subs = {      'The Office' : 'The Office (US)',
                  'Castle' : 'Castle (2009)',
              'Parenthood' : 'Parenthood (2010)',
                   'Touch' : 'Touch (2012)',
                 'Missing' : 'Missing (2012)',
       'Last Man Standing' : 'Last Man Standing (2011)'}

#interlaced channels
interlaced_chanids = ['1041', '1051', '1131']

########################################################################
#  Don't change anything below here.
########################################################################

for path in os.environ.get('PATH', '').split(':'):
    if os.path.exists(os.path.join(path, 'mythtranscode')) and \
      not os.path.isdir(os.path.join(path, 'mythtranscode')):
        mythdir = path
    if os.path.exists(os.path.join(path, 'HandBrakeCLI')) and \
      not os.path.isdir(os.path.join(path, 'HandBrakeCLI')):
        hbdir = path
    if os.path.exists(os.path.join(path, 'mkvmerge')) and \
      not os.path.isdir(os.path.join(path, 'mkvmerge')):
        mmdir = path

fmts = ['mkv', 'm4v']
#set up logging
logger = logging.getLogger('autocode')
logger.setLevel(logging.DEBUG)
syslog = SysLogHandler(address='/dev/log')
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

#parse up the inputs
parser = argparse.ArgumentParser(description='Transcode a MythTV recording to a .mp4 file with x264 video and aac and ac3 audio tracks.')
parser.add_argument("chanid", \
                    help="the channel id of the recording")
parser.add_argument("starttimeiso", \
                    help="the ISO-formatted start time of the recording")
parser.add_argument("-f", "--format", \
                    action="store", \
                    dest="fmt", \
                    default="mkv", \
                    help="the desired output container (mkv/m4v)")
parser.add_argument("-l", "--lossless", \
                    action="store_true", \
                    dest="lossless", \
                    default=False, \
                    help="put the losslessly transcoded mpeg in mkv")
parser.add_argument("-n", "--no-cuts", \
                    action="store_true", \
                    dest="nocuts", \
                    default=False, \
                    help="put the original mpeg in mkv")
parser.add_argument("-c", "--comms", \
                    action="store_true", \
                    dest="comms", \
                    default=False, \
                    help="use commercial skip list instead of cutlist")
args = parser.parse_args()

starttimeiso = args.starttimeiso
fmt = args.fmt
lossless = args.lossless
nocuts = args.nocuts
comms = args.comms

#create a temporary directory for intermediate files
tmpdir = tempfile.mkdtemp(prefix='autocode_', dir=tempdir)
logger.info("Using temp directory '%s'", tmpdir)

if fmt not in fmts:
    logger.error("Invalid output format: %s",  fmt)
    sys.exit("Invalid output format specified.")
logger.debug("start time in utc is %s", starttimeiso)

#Services API call
services_url_args = urllib.urlencode({"StartTime": starttimeiso, \
                                         "ChanId": args.chanid}, \
                                     doseq=True)
services_url = 'http://{}:{}/Dvr/GetRecorded?{}'.format(\
                          services_ip, services_port, services_url_args)
logger.debug("url = %s", services_url)
try:
    recording_info = urllib2.urlopen(services_url)
except urllib2.HTTPError, e:
    self.logger.error("Error grabbing url %s", services_url)
dom = QtXml.QDomDocument()
dom.setContent(recording_info.read())
program = dom.firstChildElement('Program')
title = str(program.firstChildElement('Title').text())
season = str(program.firstChildElement('Season').text())
episode = str(program.firstChildElement('Episode').text())
filename = str(program.firstChildElement('FileName').text())
subtitle = str(program.firstChildElement('SubTitle').text())

logger.debug('title = %s', title)
logger.debug('season = %s', season)
logger.debug('episode = %s', episode)
logger.debug('subtitle = %s', subtitle)
logger.debug('filename = %s', filename)

#parse up filename from services api
if filename is not None:
    chanid = filename.split("_")[0]
    starttime = filename.split("_")[1].rstrip(".mpg")

#setup the mythtranscode command
mythtranscode = os.path.join(mythdir, "mythtranscode")
if nocuts:
    mythtranscode_opts = "--mpeg2"
else:
    mythtranscode_opts = "--honorcutlist --mpeg2"
mythtranscode_opts_parsed = mythtranscode_opts.split()
mythtranscode_command = [mythtranscode]
for arg in mythtranscode_opts_parsed:
    mythtranscode_command.append(arg)

#setup the handbrake command
hb = os.path.join(hbdir, "HandBrakeCLI")
hb_deint = "--deinterlace"
if fmt == 'mkv':
    logger.debug("Output format will be mkv")
    hb_opts = "-e x264  -q 20.0 -r 29.97 --pfr -a 1 -E copy:ac3 -B 160 -6 auto -R Auto -D 0.0 -f mkv -4 -X 1280 --loose-anamorphic -m"
elif fmt == 'm4v':
    logger.debug("Output format will be m4v")
    hb_opts = "-e x264 -q 20.0 -r 29.97 --pfr -a 1,1 -E faac,copy:ac3 -B 160,160 -6 dpl2,auto -R Auto,Auto -D 0.0,0.0 -f mp4 -4 -X 1280 --loose-anamorphic -m"
hb_opts_parsed = hb_opts.split()
hb_command = [hb]
for arg in hb_opts_parsed:
    hb_command.append(arg)

#setup mythutil command (to get commercial cut locations)
mythutil = os.path.join(mythdir, "mythutil")
if comms:
    mythutil_opts = '-q --getskiplist --chanid {} --starttime {}'.format(chanid, starttime)
else:
    mythutil_opts = '-q --getcutlist --chanid {} --starttime {}'.format(chanid, starttime)
mythutil_opts_parsed = mythutil_opts.split()
mythutil_command = [mythutil]
for arg in mythutil_opts_parsed:
    mythutil_command.append(arg)

#get the list of cuts and parse it to make the chapter file
if chanid in interlaced_chanids:
    fps = 30000./1001.
else:
    fps = 60000./1001.
cuts = subprocess.Popen(mythutil_command, stderr=subprocess.STDOUT, \
                        stdout=subprocess.PIPE).communicate()
if comms:
    chapters = []
    slices = cuts[0].split("Commercial Skip List: ")[1].rstrip('\n').split(',')
    for slice in slices:
        for frame in slice.split('-'):
            time = int(frame) / fps
            milliseconds = int(math.floor((time - math.floor(time)) * 1000))
            seconds = int(math.floor(time))
            minutes = int(math.floor(seconds / 60.))
            hours = int(math.floor(minutes / 60.))
            seconds = seconds - minutes * 60
            minutes = minutes - hours * 60
            chapters.append((hours,minutes,seconds,milliseconds))
else:
    if nocuts:
        chapters = []
        slices = cuts[0].split("Cutlist: ")[1].rstrip('\n').split(',')
        for slice in slices:
            for frame in slice.split('-'):
                time = int(frame) / fps
                milliseconds = int(math.floor((time - math.floor(time)) * 1000))
                seconds = int(math.floor(time))
                minutes = int(math.floor(seconds / 60.))
                hours = int(math.floor(minutes / 60.))
                seconds = seconds - minutes * 60
                minutes = minutes - hours * 60
                chapters.append((hours,minutes,seconds,milliseconds))
         chapters.pop()
    else:
        chapters = [(0,0,0,0)]
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
    formatted_time = '{:0>2}:{:0>2}:{:0>2}.{:0>3}'.format(\
                      chapter[0], chapter[1], chapter[2], chapter[3])
    formatted_chapters.append(formatted_time)

#determine output filename and add it to the mythtranscode command
if title in subs: 
    title = subs[title]
output_name = '{} {:0>2}x{:0>2}'.format(title, season, episode)
tmpfile = os.path.join(tmpdir, output_name)
mythtranscode_inout = ["--chanid", chanid, "--starttime", starttime, \
                       "--outfile", "{}.mpg".format(tmpfile)]
for arg in mythtranscode_inout:
    mythtranscode_command.append(arg)

#Get the coverart for the recording
artwork = program.firstChildElement('Artwork')
artwork_infos = artwork.firstChildElement('ArtworkInfos')
artwork_info = artwork_infos.firstChildElement('ArtworkInfo')
artwork_url = None
while not artwork_info.isNull():
    type = str(artwork_info.firstChildElement('Type').text())
    if type == 'coverart':
        artwork_url = str(artwork_info.firstChildElement('URL').text())
    artwork_info = artwork_info.nextSiblingElement('ArtworkInfo')
if artwork_url is not None:
    artwork_url_arg = re.sub(' ', '%20', artwork_url)
    artwork_url =  'http://{}:{}{}'.format(services_ip, services_port, artwork_url_arg)
    logger.debug("url = %s", artwork_url)
    try:
        artwork_data = urllib2.urlopen(artwork_url)
    except urllib2.HTTPError, e:
        self.logger.error("Error grabbing url %s", artwork_url)
    cover = Image.open(StringIO.StringIO(artwork_data.read()))
    cover_filename = os.path.join(tmpdir, "{}.jpg".format(output_name))
    cover.save(cover_filename)

#see if we need to deinterlace and finish setting up handbrake command
if chanid in interlaced_chanids:
    hb_command.append(hb_deint)
if fmt == 'mkv':
    hb_inout = ["-i", "{}.mpg".format(tmpfile), "-o", "{}.mkv".format(tmpfile)]
elif fmt == 'm4v':
    hb_inout = ["-i", "{}.mpg".format(tmpfile), "-o", "{}.m4v".format(tmpfile)]
for arg in hb_inout:
    hb_command.append(arg)

#create chapter file
logger.info("Writing chapter file %s.txt.", output_name)
chap_filename = '{}.txt'.format(tmpfile)
chap_file = open(chap_filename, 'w')
if fmt == 'mkv':
    for i in range(0,len(formatted_chapters)):
        chap_file.write("CHAPTER{:0>2}={}\n".format(i + 1, formatted_chapters[i]))
        chap_file.write("CHAPTER{:0>2}NAME=Chapter {}\n".format(i + 1, i + 1))
elif fmt == 'm4v':
    for i in range(0,len(formatted_chapters)):
        chap_file.write("{} Chapter {}\n".format(formatted_chapters[i], i + 1))
chap_file.close()

#do the lossless transcode to remove cutlist
logger.info("Transcoding %s.mpg.", output_name)
subprocess.Popen(mythtranscode_command, stderr=subprocess.STDOUT,\
                     stdout=subprocess.PIPE).communicate()

if not lossless and not nocuts:
#do the transcoding with handbrake
    if fmt == 'mkv':
        logger.info("Converting '%s.mpg' to '%s.mkv'.", output_name, output_name)
    elif fmt == 'm4v':
        logger.info("Converting '%s.mpg' to '%s.m4v'.", output_name, output_name)
    subprocess.Popen(hb_command, stderr=subprocess.STDOUT,\
                     stdout=subprocess.PIPE).communicate()

#create or copy the final output file
outfile = os.path.join(output_dir, output_name)
if fmt == 'mkv':
    if os.path.isfile('{}.mkv'.format(outfile)):
        os.remove('{}.mkv'.format(outfile))
    #setup the mkvmerge command
    show_title = '{} {:0>2}x{:0>2} - {}'.format(title, season, episode, subtitle)
    mkvmerge = os.path.join(mmdir, "mkvmerge")
    mkvmerge_command = [mkvmerge]
    mkvmerge_command.append('-o')
    mkvmerge_command.append('{}.mkv'.format(outfile))
    mkvmerge_command.append('--title')
    mkvmerge_command.append(show_title)
    mkvmerge_command.append('--chapter-language')
    mkvmerge_command.append('en')
    mkvmerge_command.append('--chapters')
    mkvmerge_command.append(chap_filename)
    mkvmerge_command.append('--attach-file')
    mkvmerge_command.append(cover_filename)
    if lossless or nocuts:
        mkvmerge_command.append('{}.mpg'.format(tmpfile))
    else:
        mkvmerge_command.append('{}.mkv'.format(tmpfile))

    logger.info("Writing output to %s.mkv", outfile)
    subprocess.Popen(mkvmerge_command, \
                              stderr=subprocess.STDOUT,\
                              stdout=subprocess.PIPE).communicate()
if fmt == 'm4v':
    logger.info("Writing output files %s.{m4v, jpg, txt}", outfile)
    shutil.copyfile('{}.m4v'.format(tmpfile), '{}.m4v'.format(outfile))
    shutil.copyfile('{}.jpg'.format(tmpfile), '{}.jpg'.format(outfile))
    shutil.copyfile('{}.txt'.format(tmpfile), '{}.txt'.format(outfile))

#logger.info("Cleaning up the temporary files.")
#shutil.rmtree(tmpdir)

logger.info("Finished")

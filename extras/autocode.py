#!/usr/bin/env python

from subprocess import call
import MySQLdb
from tvshowdb import TVShowDB

#set some environment info
db_host = "localhost"
db_user = "mythtv"
db_passwd = "4Sqki5EL"
db_name = "mythconverg"
output_dir = "/var/media/videos/rips"
mythtranscode = "/usr/bin/mythtranscode"
mythtranscode_opts = "-l -m -e ps"


#setup connection to MythTV Database
conn = MySQLdb.connect (host = db_host, user = db_user, passwd = db_passwd, db = db_name)
sql = conn.cursor()

#setup connection to local tvdb database
dbTV = TVShowDB('TV.db')
dbTV.init_db()

#find all shows that have a cutlist
sql_query="SELECT title,subtitle,basename FROM recorded WHERE cutlist='1'"
sql.execute(sql_query)
reply = sql.fetchall()

#determine the output name and do the conversion
for episode in reply:
    print episode
    name = episode[1]
    episode_name = '%s%s%s' % ("'%", name, "%'")
    episode_name_wild = episode_name.replace(' ', '%')
    sql_query = "SELECT season_number,episode_number FROM episodes WHERE name LIKE %s" % (episode_name_wild,)
    out = dbTV.db_query(sql_query)
    season_ep = out[0]
    ep = (episode[2], episode[0], str(season_ep[0]).zfill(2), str(season_ep[1]).zfill(2))
    output = "%s/%s_%sx%s" % (output_dir, ep[1], ep[2], ep[3])
    call(['/usr/local/bin/xcode', ep[0], output])

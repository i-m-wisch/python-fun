#!/usr/bin/env python

import sys
import os
import glob
import sqlite3
from datetime import datetime
from prettytable import PrettyTable

basepath = "{}/.mozilla/firefox/*.default/cookies.sqlite" .format(os.environ['HOME'])
sqldb = glob.glob(basepath)[0]
MAXDATE = 2049840000

if not os.path.isfile(sqldb):
    print "Could not find cookies DB at: {}" .format(sqldb)

def epochConvert(epoch):
    date = epoch[:10]
    if int(date) > MAXDATE:
        date = str(MAXDATE)
    if len(epoch) > 10:
        time = epoch[11:]
    else:
        time = '0'
    combined = float(date+'.'+time)
    hr = datetime.fromtimestamp(combined)
    return hr.ctime()
while True:
    try:
        conn = sqlite3.connect(sqldb)
        cur = conn.cursor()
        try:
            data = cur.execute("select * from moz_cookies where baseDomain like '%rackspace%'")
        except sqlite3.Error, e:
            print 'Error {0}: ' .format(e.args[0])
            sys.exit(1)
        rackcookies = data.fetchall()

        table = PrettyTable(["ID", "Name", "Created", "Expires", "Host", "Path", "Value"])
        for cookie in rackcookies:
            expires = epochConvert(str(cookie[7]))
            created = epochConvert(str(cookie[9]))
            table.add_row([cookie[0], cookie[3], created, expires, cookie[5], cookie[6], cookie[4]])

        print table
        del_id = raw_input("\nIf you would like to delete a cookie, enter the ID, to quit hit Enter: ")
        if del_id:
            int(del_id)
            cur.execute("delete from moz_cookies where id='{}'" .format(del_id))
            conn.commit()
        else:
            conn.close()
            sys.exit(0)
    except ValueError:
        print "The ID must be numerical!"

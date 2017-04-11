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

basedom = raw_input("Enter the baseDomain you would like to search for (Default is: rackspace): ")
if not basedom:
    basedom = "rackspace"

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
            data = cur.execute("select * from moz_cookies where baseDomain like '%{}%'" .format(basedom))
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
        del_id = raw_input("\nTo delete a cookie, enter the ID. To exit, enter 'quit'. To refresh, hit Enter. INPUT: ")
        if del_id == "quit":
            conn.close()
            sys.exit(0)
        elif del_id:
            int(del_id)
            cur.execute("delete from moz_cookies where id='{}'" .format(del_id))
            conn.commit()
    except ValueError:
        print "The ID must be numerical!"

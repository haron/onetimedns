#!/usr/bin/env python

import sys, sqlite3
from datetime import date
import redis
from settings import DB

SCHEMA = """
    create table if not exists lastseen (dt date, record text unique)
"""

conn = sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = conn.cursor()
c.execute(SCHEMA)
conn.commit()

r = redis.Redis()

for k in r.keys():
    c.execute("select * from lastseen where record = ?", (k,))
    res = c.fetchone()
    if res:
        print "Saved record found, updatind date: %s" % k
        query = "update lastseen set dt = ? where record = ?"
    else:
        print "New record found, saving: %s" % k
        query = "insert into lastseen (dt, record) values (?, ?)"
    c.execute(query, (date.today(), k))
    conn.commit()

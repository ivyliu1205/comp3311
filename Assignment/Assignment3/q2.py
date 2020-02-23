# COMP3311 19T3 Assignment 3

import cs3311
import sys

# Define incommon
incommon = 2
if sys.argv[1] != 2:
    incommon = sys.argv[1]

conn = cs3311.connect()
cur = conn.cursor()

cur.execute(
    "SELECT code, courselist\
    FROM helper_q2\
    WHERE nincommon = '{}'\
    ORDER BY code".format(incommon)
)

for tup in cur.fetchall():
    code, courselist = tup
    print("{}: {}".format(code, courselist))

cur.close()
conn.close()

# COMP3311 19T3 Assignment 3

import cs3311
import math
import sys

#define term
term = '19T1'
if len(sys.argv) == 2:
    term = sys.argv[1]

conn = cs3311.connect()

cur = conn.cursor()

cur.execute(
    "SELECT count(DISTINCT roomid)\
    FROM helper_q7_time \
    WHERE term = '{}' AND totaltime >= 200 \
    ".format(term)
)

over = cur.fetchone()[0]

cur.execute(
    "SELECT count(DISTINCT r.id) \
    FROM rooms r \
    WHERE r.code LIKE 'K-%' \
    "
)

nrooms = cur.fetchone()[0]

result = round((nrooms - over) * 100/ nrooms, 1) 
print(str(result) + '%')

cur.close()
conn.close()

# COMP3311 19T3 Assignment 3

import cs3311
import sys

#define CODE
code = 'ENGG'
if len(sys.argv) == 2:
    code = sys.argv[1]

conn = cs3311.connect()
cur = conn.cursor()

cur.execute(
    "SELECT DISTINCT bname, array_agg(DISTINCT subjectcode) \
    FROM helper_q3_buildings\
    WHERE term = '19T2' AND alpha = '{}' AND bname <> 'none'\
    GROUP BY bname\
    ".format(code)
)

for tup in cur.fetchall():
    bname, subjectcode = tup
    print(bname)
    for course in subjectcode:
        print(" " + course)

cur.close()
conn.close()




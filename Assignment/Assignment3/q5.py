# COMP3311 19T3 Assignment 3

import cs3311
import sys

#define CODE
code = 'COMP1521'
if len(sys.argv) == 2:
    code = sys.argv[1]

conn = cs3311.connect()

cur = conn.cursor()

cur.execute(
    " \
    SELECT class_type, tag, CONCAT(percent, '%') \
    FROM helper_q5 \
    WHERE coursecode = '{}' AND percent < 50 \
    ".format(code)
)

for tup in cur.fetchall():
    class_type, tag, percent = tup
    print("{} {} is {} full".format(class_type, tag, percent))


cur.close()
conn.close()

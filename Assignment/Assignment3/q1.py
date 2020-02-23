# COMP3311 19T3 Assignment 3

import cs3311
conn = cs3311.connect()

cur = conn.cursor()

# TODO
query = """
    SELECT coursecode, CONCAT(round(nenrol*1.0/nquota*100,0), '%')
    FROM helper_q1
    WHERE nenrol > nquota AND nquota > 50
    GROUP BY coursecode, nenrol, nquota
    ORDER BY coursecode;
"""
cur.execute(query)
for tup in cur.fetchall():
    coursecode, concat = tup
    print("{} {}".format(coursecode, concat))

cur.close()
conn.close()

# COMP3311 19T3 Assignment 3

import cs3311
import sys

#define CODE
code = 'ENGG'
if len(sys.argv) == 2:
    code = sys.argv[1]

courseDict = {}
def addToDict(d, term, tuple):
    if term not in d:
        courseDict[term] = []
    d[term].append(tuple)

conn = cs3311.connect()

cur1 = conn.cursor()

cur1.execute(
    "SELECT term, code, nstudent\
    FROM helper_q4\
    WHERE alpha = '{}' AND term <> 'none' AND nstudent <> 0\
    ".format(code)
)

for tup in cur1.fetchall():
    term, code, nstudent = tup
    tuple = (code, nstudent)
    addToDict(courseDict, term, tuple)
    
for key, values in sorted(courseDict.items()):
    print(key)
    for value in values:
        print(" {}({})".format(value[0], value[1]))

    

cur1.close()

conn.close()

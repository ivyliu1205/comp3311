# COMP3311 19T3 Assignment 3

import cs3311

def changefixposition(list, position, newvalue):
    list[position - 1] = newvalue
    return ''.join([str(x) for x in list])

def changepartofstr(list, start, end, newvalue):
    for i in range(0, len(list)):
        if (i >= (start - 1) and i <= (end - 1)):
            list[i] = newvalue
    return ''.join([str(x) for x in list])

def divideline(str, nlist):
    splitnum = 0
    start = -1
    end = -1
    for lstr in str.split('-'):
        splitnum += 1 
        # odd - start position
        if (splitnum % 2 == 1):
            start = int(lstr)
        # even - end postion
        elif (splitnum % 2 == 0):
            end = int(lstr)
                        
        if (start >= 0 and end >= 0):
            result = changepartofstr(nlist, start, end, 1)
            start = -1
            end = -1
    return result

def transferbinary(nweek):
    newlist = [0] * 11
    
    # all zero
    if (nweek == 'N' or nweek == '>' or nweek.find('N') >= 0 or nweek.find('<') >= 0):
        result = changefixposition(newlist, 1, 0)
    # else
    else:
        # solo week
        if (nweek.find('-') < 0 and nweek.find(',') < 0):
            result = changefixposition(newlist, int(nweek), 1)
        elif (nweek.find(',') >= 0) :
            for bstr in nweek.split(','):
                # 1,2,3,4
                if (bstr.find('-') < 0):
                    result = changefixposition(newlist, int(bstr), 1)
                # 1,2,3,5-7
                else:   
                    result = divideline(bstr, newlist)
            # 1-5
        elif (nweek.find(',') < 0 and nweek.find('-') >= 0):
            result = divideline(nweek, newlist)

    return result

####################################################
conn = cs3311.connect()

cur = conn.cursor()

# SELECT
cur.execute(
    "\
    SELECT weeks, id \
    FROM meetings \
    "
)

for tup in cur.fetchall():
    weeks, mid = tup
    binaryweek = transferbinary(weeks)
    cur.execute(
        "UPDATE meetings \
        SET weeks_binary = '{}' \
        WHERE id = {} \
        ".format(binaryweek, mid)
    )
conn.commit()
cur.close()

conn.close()

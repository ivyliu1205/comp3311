# COMP3311 19T3 Assignment 3

import cs3311
import sys

#define courses
courses = []
if len(sys.argv) < 2:
    courses = ['COMP1511','MATH1131']
else:
    for i in range (1, len(sys.argv)):
        courses.append(sys.argv[i])

# 1300
def changetohour(numtime):
    time = numtime // 100 + (numtime % 100) / 60
    return time

# find relation between given classes
def timerelation(start_one, end_one, start_two, end_two):
    if (start_one < start_two):
        earlier_start = start_one
        earlier_end = end_one
        later_start = start_two
        later_end = end_two
    else:
        earlier_start = start_two
        earlier_end = end_two
        later_start = start_one
        later_end = end_one
    
    #   [ ( ] )
    if later_start >= earlier_start and later_start < earlier_end:
        return 'overlap'
    #   [ () ]
    elif later_end >= earlier_start and later_end <= earlier_end:
        return 'overlap'
    #   [   ](  )
    elif later_start == earlier_end:
        return 'adjacent'
    #   [   ]    (  )
    else:
        return later_start - earlier_end

def adapt_type(intlist):
    res = []
    for num in intlist:
        res.append(str(num))
    # print(res)
    return '{' + ','.join(res) + '}'

def sortonarray(a, b):
    n = len(a)
    for i in range(n -1):
        for j in range(1, n-1):
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                b[j - 1], b[j] = b[j], b[j - 1]

conn = cs3311.connect()
cur = conn.cursor()

cur.execute("drop table if exists helpertable;")

cur.execute(
    "\
    CREATE TABLE HELPERTABLE \
    (meetid    integer primary key not null, \
    classid     integer             not null, \
    term        text                not null, \
    courses     char(8)             not null, \
    classtype   text                not null, \
    nday        WeekDay             not null, \
    starttime   DayTime             not null, \
    endtime    DayTime             not null);"
)
conn.commit()

for cos in courses:
    cur.execute(
        " SELECT * FROM helper_q8 WHERE courses = '{}' AND term = '19T3'\
        ".format(cos)
    )

    for tup in cur.fetchall():
        meetid, classid, term, courses, classtype, nday, starttime, endtime = tup
        if (courses != None and classtype != None and nday != None):
            cur.execute(
                "INSERT INTO helpertable VALUES {}".format(tup)
            )
        conn.commit()
cur.close()

def calculateTotalhours(d):
    totalhours = 0
    for key, values in d.items():
        if (len(values) > 0):
            values.sort(key=lambda tup:tup[2])
            totalhours += 2
            totalhours += changetohour(values[-1][3]) - changetohour(values[0][2])
    return totalhours


def printfinalanswer(d):
    totalhours = 0
    cur7 = conn.cursor()
    weekday = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    weekDict = {}
    for key, values in d.items():
        for midlist in values:
            for mid in midlist:
                cur7.execute("SELECT courses, classtype, nday, starttime, endtime FROM helpertable WHERE meetid = {}".format(mid))
                for tple in cur7.fetchall():
                    courses, classtype, nday, start, end = tple
                    tuple = (courses, classtype, start, end)
                    if nday not in weekDict:
                        weekDict[nday] = []
                    weekDict[nday].append(tuple)
    
    print('Total hours: {}'.format(calculateTotalhours(weekDict)))
    for day in weekday:
        for key, values in weekDict.items():
            values.sort(key=lambda tup:tup[2])
            if (day == key and len(values) > 0):
                print('  {}'.format(day))
                for vtup in values:
                    print('    {} {}: {}-{}'.format(vtup[0], vtup[1], vtup[2], vtup[3]))
                
    
    cur7.close()


cur1 = conn.cursor()

# [coursetype, nday, starttime, endtime]
coursetypeDict = {}
finalDict = {}

cur1.execute(
    "SELECT courses, classtype, array_agg(meetid) AS midlist FROM helpertable GROUP BY classid, courses, classtype "
)

for tup in cur1.fetchall():
    courses, classtype, meetid= tup
    keyname = courses + classtype
    if keyname not in coursetypeDict:
        coursetypeDict[keyname] = []
        finalDict[keyname] = []
    coursetypeDict[keyname].append(meetid)

'''
for key, value in coursetypeDict.items():
    print(key)
    print(value)
print('##############################')
''' '''
for key, value in finalDict.items():
    print(key)
print('##############################')
'''
cur1.close()

cur2 = conn.cursor()
'''
tempList = []
for key, value in coursetypeDict.items():
    for mid in value[0]:
        tempList.append(mid)
        continue 
'''
cur2.execute("drop table if exists helperelation;")

cur2.execute(
    "\
    CREATE TABLE HELPERELATION \
    (classid    integer primary key not null, \
    course      text                not null, \
    classtype   text                not null, \
    meetid      integer ARRAY       not null, \
    adjacentmid integer ARRAY               , \
    closemid    integer ARRAY               , \
    overlapmid  integer ARRAY               );"
)
conn.commit()

for key, value in coursetypeDict.items():
    # midlist
    for midlist in value:
        classid = -1
        classtype = None
        course = None
        adjacentmid = []
        closemid = []
        overlapmid = []
        for mid in midlist:
            cur5 = conn.cursor()
            cur5.execute(
                "SELECT classid, courses, classtype, nday, starttime, endtime \
                FROM helpertable \
                WHERE meetid = {} \
                ".format(mid)
            )
            currstart = currend = otherstart = otherend = -1
            for tup in cur5.fetchall():
                cid, co, cltp, nday, start, end = tup
                currstart = start
                currend = end
                course = co
                classtype = cltp
                classid = cid
            if (currstart > 0 and currend > 0):
                for subkey, subvalue in coursetypeDict.items():
                    if (subkey != key):
                        for submidlist in subvalue:
                            cur6 = conn.cursor()
                            for submid in submidlist:
                                cur6.execute(
                                    "SELECT nday, starttime, endtime \
                                    FROM helpertable \
                                    WHERE meetid = {} \
                                    ".format(submid)
                                )
                                for subtup in cur6.fetchall():
                                    subday, substart, subend = subtup
                                    otherstart = substart
                                    otherend = subend
                                # print(currstart + currend + otherstart + otherend)
                                if (subday == nday):
                                    if (timerelation(currstart, currend, otherstart, otherend) == 'adjacent'):
                                        adjacentmid.append(submid)
                                    elif (timerelation(currstart, currend, otherstart, otherend) == 'overlap'):
                                        overlapmid.append(submid)
                                    else:
                                        difference = timerelation(currstart, currend, otherstart, otherend)
                                        closemid.append(submid)
                                else:
                                    overlapmid.append(submid)
                            cur6.close()
            cur5.close()

        tple = (classid, course, classtype, adapt_type(midlist), adapt_type(adjacentmid), adapt_type(closemid), adapt_type(overlapmid))
        cur2.execute(
            "INSERT INTO HELPERELATION VALUES {}".format(tple)
        )
        conn.commit()

cur2.close()
# printfinalanswer(tempList)

def findKey(meetid):
    cur5 = conn.cursor()
    cur5.execute("SELECT CONCAT(courses, classtype) FROM helpertable WHERE meetid = {}".format(meetid))
    for tup in cur5.fetchall():
        keylist = tup
        key = keylist[0]
    cur5.close()
    return key

def findsamecid(meetid):
    samecid = []
    cur5 = conn.cursor()
    cur5.execute("SELECT meetid FROM helpertable WHERE classid = (SELECT classid FROM helpertable WHERE meetid = {})".format(meetid))
    for tup in cur5.fetchall():
        mid = tup
        for this in mid:
            samecid.append(this)
    cur5.close()
    return samecid

# not overlap -> true or overlap -> false
def checkoverlap(midlist, newmid):
    cur6 = conn.cursor()
    cur6.execute(
        "SELECT nday, starttime, endtime FROM helpertable WHERE meetid = {}".format(newmid)
    )

    for tup in cur6.fetchall():
        day, startlist, endlist = tup
        newstart = startlist
        newend = endlist
    #print('new mid {}'.format(newmid))
    #print('start {}'.format(startlist))
    #print('end {}'.format(endlist))
    for mid in midlist:
        cur6.execute(
            "SELECT nday, starttime, endtime FROM helpertable WHERE meetid = {}".format(mid)
        )

        for tup in cur6.fetchall():
            olday, startlist, endlist = tup
            oldstart = startlist
            oldend = endlist

        if (olday == day and timerelation(newstart, newend, oldstart, oldend) == 'overlap'):
            return False
    return True

def removeitemindict(d):
    for key in d.keys():
        d.pop(key)
        d[key] = []
    return d

cur3 = conn.cursor()
cur3.execute("drop table if exists helperkey;")

cur3.execute(
    "\
    CREATE TABLE HELPERKEY \
    (meetid     integer primary key not null, \
    nkey         text                not null, \
    adjacentmid integer ARRAY               , \
    closemid    integer ARRAY               , \
    overlapmid  integer ARRAY               );"
)

def check_dictfinished(d):
    length = 0
    for key, value in d.items():
        if (len(value) > 0):
            length += 1

    if (length == len(d.keys())):
        return True
    else:
        return False

conn.commit()
cur3.execute(
    "SELECT CONCAT(course, classtype), unnest(meetid), adjacentmid, closemid, overlapmid FROM helperelation \
    "
)

for tup in cur3.fetchall():
    key, meetid, adjacentmid, closemid, overlapmid = tup
    tple = (meetid, key, adapt_type(adjacentmid), adapt_type(closemid), adapt_type(overlapmid))
    cur3.execute(
        "INSERT INTO HELPERKEY VALUES {}".format(tple)
    )
    conn.commit()

# only search the values of first key in courseDict
cur3.execute("SELECT meetid, nkey, adjacentmid, closemid FROM helperkey")
alreadyindict = []
for tup in cur3.fetchall():
    meetid, key, adjacentmid, closemid = tup
    print('##################') 
    print(meetid)
    print('##################') 
    if (len(alreadyindict) == 0):
        for samecmid in findsamecid(meetid):
            alreadyindict.append(meetid)
    finalDict[key].append(findsamecid(meetid))

    if (len(adjacentmid) > 0):
        for adjacent_mid in adjacentmid:
            if (findKey(adjacent_mid) != key):
                appendOK = True
                for samekey_mid in findsamecid(adjacent_mid):
                    if (checkoverlap(alreadyindict, samekey_mid) == False or len(finalDict[findKey(adjacent_mid)]) == 1):
                        appendOK = False
                        break

                if (appendOK == True and len(finalDict[findKey(adjacent_mid)]) == 0):
                    for appendmid in findsamecid(adjacent_mid):
                        alreadyindict.append(appendmid)
                    finalDict[findKey(adjacent_mid)].append(findsamecid(adjacent_mid))
        for key, values in finalDict.items():
            print(key)
            print(values)
        print('##################')      
    if (len(closemid) > 0):
    # SEARCH closemid
        for close_mid in closemid:
            if (findKey(close_mid) != key):
                appendOK = True

                for samekey_mid in findsamecid(close_mid):
                    if (checkoverlap(alreadyindict, samekey_mid) == False or len(finalDict[findKey(samekey_mid)]) == 1):
                        #print('appendOk false')
                        appendOK = False
                        break

                if (appendOK == True and len(finalDict[findKey(close_mid)]) == 0):
                    #print('append')
                    for appendmid in findsamecid(close_mid):
                        alreadyindict.append(appendmid)
                    finalDict[findKey(close_mid)].append(findsamecid(close_mid))

    
        for key, values in finalDict.items():
            print(key)
            print(values)
        print('##################')  

    # check the final dict is finished or not
    if (check_dictfinished(finalDict) == True):
        #print('final finished')
        break
    else:
        #print('final not finished, need clear list')
        removeitemindict(finalDict)
        alreadyindict.clear()

printfinalanswer(finalDict)
cur3.execute("drop table if exists helpertable;")
cur3.execute("drop table if exists helperelation;")
cur3.execute("drop table if exists helperkey;")

cur3.close()
conn.close()

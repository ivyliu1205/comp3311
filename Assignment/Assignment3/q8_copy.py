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

def printfinalanswer(d):
    weekDict = {}
    weekDay = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    monday = []
    monend = []
    monorder = []
    tueday = []
    tueend = []
    tueorder = []
    wedday = []
    wedend = []
    wedorder = []
    thuday = []
    thuend = []
    thuorder = []
    friday = []
    friend = []
    friorder = []
    satday = []
    satend = []
    satorder = []
    sunend = []
    sunday = []
    sunorder = []
    totalhours = 0
    cur0 = conn.cursor()
    
    for key, values in d.items():
        list = values[0]
        for mid in list:
            cur0.execute(
                "SELECT courses, classtype, nday, starttime, endtime, CONCAT(CONCAT(starttime,'-'),endtime) \
                FROM helpertable WHERE meetid = {}\
                ".format(mid)
            )

            for tup in cur0.fetchall():
                courses, classtype, nday, start, end, time = tup
                resultstr = courses + ' ' + classtype + ': ' + time
                if (nday == 'Mon'):
                    monday.append(resultstr)
                    monorder.append(start)
                    monend.append(end)
                elif (nday == 'Tue'):
                    tueday.append(resultstr)
                    tueorder.append(start)
                    tueend.append(end)
                elif (nday == 'Wed'):
                    wedday.append(resultstr)
                    wedorder.append(start)
                    wedend.append(end)
                elif (nday == 'Thu'):
                    thuday.append(resultstr)
                    thuorder.append(start)
                    thuend.append(end)
                elif (nday == 'Fri'):
                    friday.append(resultstr)
                    friorder.append(start)
                    friend.append(end)
                elif (nday == 'Sat'):
                    satday.append(resultstr)
                    satorder.append(start)
                    satend.append(end)
                else:
                    sunday.append(resultstr)
                    sunorder.append(start)
                    sunend.append(end)               

    if (len(monday) > 0):
        sortonarray(monorder, monday)
        totalhours = totalhours + 2 + (changetohour(max(monend)) - changetohour(min(monorder)))
    if (len(tueday) > 0):
        sortonarray(tueorder, tueday)
        totalhours = totalhours + 2 + (changetohour(max(tueend)) - changetohour(min(tueorder)))
    if (len(wedday) > 0):
        sortonarray(wedorder, wedday)
        totalhours = totalhours + 2 + (changetohour(max(wedend)) - changetohour(min(wedorder)))
    if (len(thuday) > 0):
        sortonarray(thuorder, thuday)
        totalhours = totalhours + 2 + (changetohour(max(thuend)) - changetohour(min(thuorder)))
    if (len(friday) > 0):
        sortonarray(friorder, friday)
        totalhours = totalhours + 2 + (changetohour(max(friend)) - changetohour(min(friorder)))
    if (len(satday) > 0):
        sortonarray(satorder, satday)
        totalhours = totalhours + 2 + (changetohour(max(satend)) - changetohour(min(satorder)))
    if (len(sunday) > 0):
        sortonarray(sunorder, sunday)
        totalhours = totalhours + 2 + (changetohour(max(sunend)) - changetohour(min(sunorder)))
    
    print('Total hours: {}'.format(totalhours))
    if (len(sunday) > 0):
        print('  Sun')
        for res in sunday:
            print('    ' + res)
    
    if (len(monday) > 0):
        print('  Mon')
        for res in monday:
            print('    ' + res)

    if (len(tueday) > 0):
        print('  Tue')
        for res in tueday:
            print('    ' + res)
    
    if (len(wedday) > 0):
        print('  Wed')
        for res in wedday:
            print('    ' + res)
    
    if (len(thuday) > 0):
        print('  Thu')
        for res in thuday:
            print('    ' + res)
    
    if (len(friday) > 0):
        print('  Fri')
        for res in friday:
            print('    ' + res)

    if (len(satday) > 0):
        print('  Sat')
        for res in satday:
            print('    ' + res)

    cur0.close()



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

def checkoverlap(midlist, newmid):
    cur6 = conn.cursor()
    cur6.execute(
        "SELECT nday, starttime, endtime FROM helpertable WHERE meetid = {}".format(newmid)
    )

    for tup in cur6.fetchall():
        day, startlist, endlist = tup
        newstart = startlist
        newend = endlist

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
    key         text                not null, \
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

cur3.execute(
    "SELECT CONCAT(course, classtype), meetid FROM helperelation"
)

changeOK = True
for tup in cur3.fetchall():
    key, midlist = tup
    if changeOK == True:
        alreadyindict = []
        finalDict[key].append(midlist)
        for mid in midlist:
            alreadyindict.append(mid)
        changeOK == False
    cur4 = conn.cursor()
    for mid in midlist:
        cur4.execute(
            "SELECT adjacentmid, closemid, overlapmid FROM helperkey WHERE meetid = {}".format(mid)
        )
    
    for tple in cur4.fetchall():
        alist, clist, olist = tple
        # search adjacent list first
        if (len(alist) > 0):
            for mid in alist:
                if (findKey(mid) != key and checkoverlap(alreadyindict, mid) == True):
                    thiskey = findKey(mid)
                    samec = findsamecid(mid)
                    appendOK = False
                    for everymid in samec:
                        if (checkoverlap(alreadyindict, everymid) == True):
                            appendOK = True
                        else:
                            appendOK = False
                            break
                    if (appendOK == True):
                        finalDict[thiskey].append(samec)
                
                if (check_dictfinished(finalDict) == True):
                    break

        # Then search close list
        else:
            for mid in sortedclist:
                if (findKey(mid) != key and checkoverlap(alreadyindict, mid) == True):
                    thiskey = findKey(mid)
                    samec = findsamecid(mid)
                    appendOK = False
                    for everymid in samec:
                        if (checkoverlap(alreadyindict, everymid) == True):
                            appendOK = True
                        else:
                            appendOK = False
                            break
                    if (appendOK == True):
                        finalDict[thiskey].append(samec)
                    
                if (check_dictfinished(finalDict) == True):
                    break

            if (check_dictfinished(finalDict) == True):
                changeOK = False
                break
            else:
                finalDict = removeitemindict(finalDict)
                changeOK = True
                        
    cur4.close()

printfinalanswer(finalDict)
cur3.execute("drop table if exists helpertable;")
cur3.execute("drop table if exists helperelation;")
cur3.execute("drop table if exists helperkey;")

cur3.close()
conn.close()

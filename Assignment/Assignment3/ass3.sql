-- COMP3311 19T3 Assignment 3
-- Helper views and functions (if needed)

-- Helper view of q1
-- create a view of coursecode, number of enrolment students and quota
CREATE OR REPLACE VIEW helper_q1(coursecode, term, nenrol, nquota)
AS
    SELECT s.code AS coursecode, t.name As term, count(DISTINCT e.person_id) AS nenrol, c.quota AS nquota
    FROM subjects s, course_enrolments e, courses c, terms t
    WHERE e.course_id = c.id AND c.term_id = t.id AND s.id = c.subject_id AND t.name = '19T3'
    GROUP BY coursecode, term, nquota;
;

-- Helper view of q2
-- Divide coursecode to alphabetical part and numerical part
CREATE OR REPLACE VIEW helper_q2_dividecode(alpha, num, subjectcode, subject_id)
AS
    SELECT left(code, 4) as alpha, right(code, 4) as num, code as subjectcode, id as subject_id
    FROM subjects;
;

-- create a view of incommon code number, number of incommon code and list of incommon coursecode's alphabetical part
CREATE OR REPLACE VIEW helper_q2(code, nincommon, courselist)
AS
    SELECT num AS code, count(DISTINCT alpha) AS nincommon, array_to_string(array_agg(DISTINCT alpha ORDER BY alpha),' ' ) AS courselist
    FROM helper_q2_dividecode
    GROUP BY code;
;

-- Helper view of q3
-- create a view of courses and its location
CREATE OR REPLACE VIEW helper_q3_buildings(subjectcode, alpha, term, bname)
AS
    SELECT helper_q2_dividecode.subjectcode AS subjectcode, helper_q2_dividecode.alpha as alpha, terms.name as term, buildings.name as bname
    FROM helper_q2_dividecode
    FULL OUTER JOIN courses ON courses.subject_id = helper_q2_dividecode.subject_id
    FULL OUTER JOIN terms ON courses.term_id = terms.id
    FULL OUTER JOIN classes ON classes.course_id = courses.id
    FULL OUTER JOIN meetings ON meetings.class_id = classes.id
    FULL OUTER JOIN rooms ON rooms.id = meetings.room_id
    FULL OUTER JOIN buildings ON rooms.within = buildings.id;
;

-- Helper view of q4
CREATE OR REPLACE VIEW helper_q4(term, alpha, code, nstudent)
AS
    SELECT terms.name AS term, left(subjects.code, 4) AS alpha,subjects.code AS code, count(DISTINCT course_enrolments.person_id) AS nstudent
    FROM terms
    FULL OUTER JOIN courses ON courses.term_id = terms.id
    FULL OUTER JOIN subjects ON courses.subject_id = subjects.id
    FULL OUTER JOIN course_enrolments ON course_enrolments.course_id = courses.id
    GROUP By term, code;
;

-- Helper view of q5
CREATE OR REPLACE VIEW helper_q5(coursecode, class_type, tag, percent)
AS
    SELECT s.code AS coursecode, ct.name AS class_type, c.tag AS tag, round(count(DISTINCT e.person_id)*1.0/c.quota*100, 0) As percent
    FROM subjects s,classtypes ct, classes c, class_enrolments e, terms t, courses co
    WHERE c.type_id = ct.id AND e.class_id = c.id AND t.name = '19T3' AND c.course_id = co.id AND co.term_id = t.id AND co.subject_id = s.id
    GROUP BY coursecode, class_type, c.tag, c.quota
    ORDER BY class_type, tag, percent;
;

-- Helper view of q7
CREATE OR REPLACE VIEW helper_q7_rearrange(roomid, term, room, nday, start_time, end_time, bweek)
AS
    SELECT rooms.id AS roomid, terms.name as term, rooms.code AS room, meetings.day as nday, meetings.start_time AS starttime, meetings.end_time AS endtime, meetings.weeks_binary AS bweek
    FROM rooms 
    FULL OUTER JOIN meetings ON meetings.room_id = rooms.id
    LEFT OUTER JOIN classes ON meetings.class_id = classes.id
    LEFT OUTER JOIN courses ON classes.course_id = courses.id
    LEFT OUTER JOIN terms ON courses.term_id = terms.id;
;

CREATE OR REPLACE VIEW helper_q7_time(roomid, room, term, totaltime)
AS
    SELECT roomid AS roomid, room AS room, term AS term,
        sum(((end_time/100 + round((end_time%100::numeric/60::numeric),2)) - 
        (start_time/100 + round((start_time%100::numeric/60::numeric),2))) * 
        (array_length(regexp_split_to_array(left(bweek,10), '1'), 1) - 1)) AS totaltime       
    FROM helper_q7_rearrange
    WHERE room LIKE 'K-%'
    GROUP BY roomid, room, term;
;

-- Helper view of q8
CREATE OR REPLACE VIEW helper_q8(meetid, classid, term, courses, classtype, nday, starttime, endtime)
AS
    SELECT meetings.id AS meetid, classes.id AS classid, terms.name AS term, subjects.code AS courses, classtypes.name AS classtype, meetings.day AS nday, meetings.start_time AS starttime, meetings.end_time AS endtime
    FROM subjects
    FULL OUTER JOIN courses ON courses.subject_id = subjects.id
    LEFT JOIN terms ON terms.id = courses.term_id
    LEFT JOIN classes ON courses.id = classes.course_id
    LEFT JOIN classtypes ON classtypes.id = classes.type_id
    LEFT JOIN meetings ON meetings.class_id = classes.id
    ORDER BY meetings.day;
;


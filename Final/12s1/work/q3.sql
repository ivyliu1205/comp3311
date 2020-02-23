-- COMP3311 12s1 Exam Q3
-- The Q3 view must have attributes called (team,players)

-- Write an SQL view that gives the country name of the team which has
-- the most players who have never scored a goal.
-- The view should show the number of goal-less players, as well as the country name.

drop view if exists Q3_helper;
create view Q3_helper
as
    SELECT t.country AS team, p.id AS players, count(DISTINCT g.id) AS ngoal
    FROM teams t, players p, goals g
    WHERE p.memberOf = t.id AND g.scoredBy = p.id
    GROUP BY p.id;
;

drop view if exists Q3_helper_ngoaless;
create view Q3_helper_ngoaless
AS
    SELECT t.country AS team, count(DISTINCT p.id) AS players
    FROM teams t, players p
    WHERE p.memberOf = t.id AND p.id not in(
                                    SELECT players FROM Q3_HELPER
                                )
    GROUP BY team;
;

drop view if exists Q3;
create view Q3
as
    SELECT team, max(players)
    FROM Q3_helper_ngoaless;
;

-- COMP3311 19T3 Assignment 2
-- Written by <<Yiting Liu>>

-- Q1 Which movies are more than 6 hours long? 

create or replace view Q1(title)
as
	SELECT t.main_title AS title
	FROM titles t
	WHERE t.runtime > 360 AND t.format = 'movie'
	ORDER BY title;
;


-- Q2 What different formats are there in Titles, and how many of each?

create or replace view Q2(format, ntitles)
as
	SELECT Distinct(t.format) AS format, count(format) as ntitles
	FROM titles t
	GROUP BY format
	ORDER BY format;
;


-- Q3 What are the top 10 movies that received more than 1000 votes?

create or replace view Q3(title, rating, nvotes)
as
	SELECT t.main_title AS title, t.rating AS rating, t.nvotes AS nvotes
	FROM titles t
	WHERE t.nvotes > 1000 AND t.format = 'movie'
	ORDER BY rating DESC, title
	LIMIT 10;
;


-- Q4 What are the top-rating TV series and how many episodes did each have?
-- 	   -the rating is based on the overall rating for the series
--	   -the ratings of individual episodes are not relevant for this
--	   -"TV series" includes both regular TV series and TV mini-series

create or replace view Q4(title, nepisodes)
as
	SELECT t.main_title as title, count(e.episode)::Counter AS nepisodes
	FROM episodes e, helper_toprating_tvseries t
	WHERE t.id = e.parent_id
	GROUP BY t.main_title;
;


-- Used to find top rating tvSeries
create or replace view helper_toprating_tvseries
AS
	SELECT *
	FROM titles
	WHERE 
		(format = 'tvSeries' OR format = 'tvMiniSeries') 
		AND rating = 10;
;

-- Q5 Which movie was released in the most languages?

create or replace view Q5(title, nlanguages)
as
	SELECT mtitle as title, nlan AS nlanguages
	FROM helper_title_nlanguage
	WHERE nlan = (SELECT max(nlan) FROM helper_title_nlanguage)
	GROUP BY title, nlan;
;

-- Used to find movies' titles and the number of its language
create or replace view helper_title_nlanguage(mtitle, nlan)
AS
	SELECT main_title AS mtitle, count(DISTINCT a.language) AS nlan
	FROM titles t, aliases a
	WHERE t.format = 'movie' AND t.id = a.title_id
	GROUP BY mtitle;
;
-- Q6 Which actor has the highest average rating in movies that they're known for?

create or replace view Q6(name)
as
	SELECT actor_name
	FROM helper_summary
	WHERE nmovie > 1
		AND average = (
			SELECT max(average)
			FROM helper_summary
			WHERE nmovie > 1
		)
	GROUP BY actor_name;
;

-- Used to find actors' names and the number of their known_for movies and its average ratings
create or replace view helper_summary(actor_name, nmovie, average)
AS
	SELECT n.name AS actor_name, count(t.main_title) AS nmovie, round(sum(t.rating)::numeric/count(t.main_title)::numeric) AS average
	FROM names n, worked_as w, titles t, known_for k
	WHERE w.work_role = 'actor' 
		AND t.format = 'movie'
		AND n.id = w.name_id 
		AND k.name_id = n.id
		AND t.id = k.title_id
	GROUP BY actor_name;
;
-- Q7 For each movie with more than 3 genres, show the movie title and a comma-separated list of the genres

create or replace view Q7(title,genres)
as
	SELECT t.main_title AS title, string_agg(DISTINCT g.genre, ',' ORDER BY g.genre) AS genres
	FROM titles t, title_genres g
	WHERE t.format = 'movie'
		AND t.id = g.title_id 
	GROUP BY t.id
	HAVING count(DISTINCT g.genre) > 3
	ORDER BY title;
;


-- Q8 Get the names of all people who had both actor and crew roles on the same movie

create or replace view Q8(name)
as
	SELECT DISTINCT n.name AS name
	FROM names n, actor_roles a, crew_roles c, titles t
	WHERE n.id = a.name_id
		AND n.id = c.name_id
		AND t.format = 'movie'
		AND a.title_id = c.title_id
		AND a.title_id = t.id;
;

-- Q9 Who was the youngest person to have an acting role in a movie, and how old were they when the movie started?

create or replace view Q9(name,age)
as
	SELECT person, age
	FROM helper_age
	WHERE age = (
		SELECT min(age)
		FROM helper_age
		WHERE age >= 0
	)
	GROUP BY person, age;
;

-- Used to get the casts' name and their ages when the movie started shooting
create or replace view helper_age(person, age)
as
	SELECT n.name AS person, t.start_year - n.birth_year AS age
	FROM names n, titles t, actor_roles a
	WHERE n.id = a.name_id
		AND t.id = a.title_id
		AND t.format = 'movie';
;

-- Q10 Write a PLpgSQL function that, given part of a title, shows the full title and the total size of the cast and crew

create or replace function
	Q10(partial_title text) returns setof text
as $$
	declare
		found integer := 0;
		tuple record;
		result_text text := NULL;
	begin
		for tuple in
			SELECT *
			FROM helper_workersummary
			WHERE title ilike '%'||partial_title||'%'
		loop
			if (tuple is NULL) then
				EXIT;
			end if;
			found := 1;
			result_text := concat(tuple.title, ' has ', tuple.nworker, ' cast and crew');
			return next result_text;
		end loop;

		if (found = 0) then
			result_text := 'No matching titles';
			return next result_text;
		end if;
	end;
$$ language plpgsql;

-- Used to create a view with titles and their workers' ID
create or replace view helper_aggregation
AS
	SELECT titles.id AS titleid, titles.main_title AS title, actor_roles.name_id AS castid, crew_roles.name_id AS crewid, principals.name_id AS principalid
	FROM titles
	FULL OUTER JOIN actor_roles ON titles.id = actor_roles.title_id
	FULL OUTER JOIN crew_roles ON titles.id = crew_roles.title_id
	FULL OUTER JOIN principals ON titles.id = principals.title_id
	ORDER BY titleid;
;

-- Used to combine workers' id
create or replace view helper_union
AS
	SELECT titleid AS titleid, title AS title, castid AS workerid
	FROM helper_aggregation
	WHERE castid is not NULL
	UNION
		SELECT titleid, title, crewid FROM helper_aggregation WHERE crewid is not NULL
	UNION 
		SELECT titleid, title, principalid FROM helper_aggregation WHERE principalid is not NULL
	ORDER by title;
;

-- Used to create a view of titles and the number of their workers
create or replace view helper_workersummary
AS
	SELECT titleid AS id, title AS title, count(DISTINCT workerid) AS nworker
	FROM helper_union
	GROUP BY id, title;
;
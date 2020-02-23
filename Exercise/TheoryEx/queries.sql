-- Q1.  What beers are made by Toohey's?

select name
from   Beers
where  manf = 'Toohey''s';


-- Q2.  Find the brewers whose beers John likes.

select distinct b.manf
from   Beers b, Likes L, Drinkers d
where  d.name = 'John' and d.id = L.drinker
	and L.beer = b.id;

-- Q3.  Find the beers sold at bars where John drinks.

select distinct b.name
from   Beers b, Sells s, Frequents f, Drinkers d
where  d.name = 'John' and d.id = f.drinker
        and f.bar = s.bar and s.beer = b.id;


-- Q4.  How many drinkers are there in each suburb?

select address,count(*)
from   Drinkers group by address;


-- Q5.  What is the name of the cheapest beer at each bar?


-- Q6.  Which beers are sold at all bars?

select distinct s.beer
from   Sells s
where  not exists (
	 (select id from Bars)
	except
	 (select bar from Sells where beer = s.beer)
	);


-- Q7.  How many bars are there in suburbs where drinkers live?
--      (Must include suburbs where there are no bars) 

select d.addr, count(b.name)
from   Drinkers d left outer join Bars b using (addr)
group  by d.addr;


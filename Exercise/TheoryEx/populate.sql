--
--  This script creates the Beer database 
--
--  Run it via:  \i populate.sql
--
--  Assume that the schema.sql script has just been run
--  and that the database contains all empty tables
--

insert into Beers values
	(1,'80/-', 'Caledonian');
insert into Beers values
	(2,'Bigfoot Barley Wine', 'Sierra Nevada');
insert into Beers values
	(3,'Burragorang Bock', 'George IV Inn');
insert into Beers values
	(4,'Crown Lager', 'Carlton');
insert into Beers values
	(5,'Fosters Lager', 'Carlton');
insert into Beers values
	(6,'Invalid Stout', 'Carlton');
insert into Beers values
	(7,'Melbourne Bitter', 'Carlton');
insert into Beers values
	(8,'New', 'Toohey''s');
insert into Beers values
	(9,'Old', 'Toohey''s');
insert into Beers values
	(10,'Old Admiral', 'Lord Nelson');
insert into Beers values
	(11,'Pale Ale', 'Sierra Nevada');
insert into Beers values
	(12,'Premium Lager', 'Cascade');
insert into Beers values
	(13,'Red', 'Toohey''s');
insert into Beers values
	(14,'Sheaf Stout', 'Toohey''s');
insert into Beers values
	(15,'Sparkling Ale', 'Cooper''s');
insert into Beers values
	(16,'Stout', 'Cooper''s');
insert into Beers values
	(17,'Three Sheets', 'Lord Nelson');
insert into Beers values
	(18,'Victoria Bitter', 'Carlton');


insert into Bars values
	(1,'Australia Hotel', 'The Rocks', '123456');
insert into Bars values
	(2,'Coogee Bay Hotel', 'Coogee', '966500');
insert into Bars values
	(3,'Lord Nelson', 'The Rocks', '123888');
insert into Bars values
	(4,'Marble Bar', 'Sydney', '122123');
insert into Bars values
	(5,'Regent Hotel', 'Kingsford', '987654');
insert into Bars values
	(6,'Royal Hotel', 'Randwick', '938500');


insert into Drinkers values
	(1,'Adam', 'Randwick', '9385-4444');
insert into Drinkers values
	(2,'Gernot', 'Newtown', '9415-3378');
insert into Drinkers values
	(3,'John', 'Clovelly', '9665-1234');
insert into Drinkers values
	(4,'Justin', 'Mosman', '9845-4321');


insert into Likes values (1, 4);
insert into Likes values (1, 5);
insert into Likes values (1, 8);
insert into Likes values (2, 12);
insert into Likes values (2, 15);
insert into Likes values (3, 1);
insert into Likes values (3, 2);
insert into Likes values (3, 11);
insert into Likes values (3, 17);
insert into Likes values (4, 15);
insert into Likes values (4, 18);


insert into Sells values (1, 3, 3.50);
insert into Sells values (2, 8, 2.25);
insert into Sells values (2, 9, 2.50);
insert into Sells values (2, 15, 2.80);
insert into Sells values (2, 18, 2.30);
insert into Sells values (3, 17, 3.75);
insert into Sells values (3, 10, 3.75);
insert into Sells values (4, 8, 2.80);
insert into Sells values (4, 9, 2.80);
insert into Sells values (4, 18, 2.80);
insert into Sells values (5, 8, 2.20);
insert into Sells values (5, 18, 2.20);
insert into Sells values (6, 8, 2.30);
insert into Sells values (6, 9, 2.30);
insert into Sells values (6, 18, 2.30);


insert into Frequents values (1, 2);
insert into Frequents values (2, 3);
insert into Frequents values (3, 2);
insert into Frequents values (3, 3);
insert into Frequents values (3, 1);
insert into Frequents values (4, 5);
insert into Frequents values (4, 4);


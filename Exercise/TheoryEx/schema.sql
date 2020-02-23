create table Beers (
    id      integer primary key,
    name    varchar(30),
    manf    varchar(20)
);
create table Bars (
    id      integer primary key,
    name    varchar(30),
    addr    varchar(20),
    license integer
);
create table Drinkers (
    id      integer primary key,
    name    varchar(20),
    addr    varchar(30),
    phone   char(10)
);
create table Sells (
    bar     integer references Bars(id),
    beer    integer references Beers(id),
    price   real,
    primary key (bar,beer)
);
create table Likes (
    drinker integer references Drinkers(id),
    beer    integer references Beers(id),
    primary key (drinker,beer)
);
create table Frequents (
    drinker integer references Drinkers(id),
    bar     integer references Bars(id),
    primary key (drinker,bar)
);

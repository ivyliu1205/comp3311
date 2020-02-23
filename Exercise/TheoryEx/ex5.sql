-- Q1
create or replace function
    sqr(x numeric) returns numeric
as $$
declare
    result numeric;
begin
    result := x * x;
    return result;
end;
$$ language plpgsql;

-- Q2
-- recursive
create or replace function
    fac(x integer) returns integer
as $$
begin
    if (x < 0) then
        return NULL;
    elsif (x = 1) then
        return 1;
    elsif (x = 0) then
        return 1;
    else
        return x * fac(x - 1);
    end if;
end;
$$ language plpgsql;

-- iterative
create or replace function
    fac(x integer) returns integer
as $$
declare
    i integer;
    res integer;
begin
    if (x < 0) then
        return NULL;
    else
        res := 1;
        for i in 1..x loop
            res := res * i;
        end loop;
        return res;
    end if;
end;
$$ language plpgsql;

-- Q3
create or replace function
    spread(input text) returns text
as $$
declare
    result text;
    i   integer;
    le  integer;
begin
    result := '';
    i := 1;
    le := length(input);
    while (i <= le) loop
        result := result || substr(input, i, 1) || ' ';
        i := i + 1;
    end loop;
    return result;
end;
$$ language plpgsql;

-- Q4
create type IntValue as ( val integer );

create or replace function 
    seq(int) returns setof IntValue
as $$
declare
    i   integer;
    res IntValue%rowtype;
begin
    for i in 1..$1 loop
        res.val := i;
        return next res;
    end loop;
end;
$$ language plpgsql;

-- q5
create or replace function 
    seq(int,int,int) returns setof IntValue
as $$
declare
    lo alias for $1;
    hi alias for $2;
    inc alias for $3;
    i integer;
    res IntValue%rowtype;
begin
    if (inc = 0) then
        return next NULL;
    elsif (inc < 0) then
        i := hi;
        while (i >= lo) loop
            res.val := i;
            return next res;
            i := i + inc;
        end loop;
    else
        i := lo;
        while (i <= hi) loop
            res.val := i;
            return next res;
            i := i + inc;
        end loop;
    end if;
end;
$$ language plpgsql;

-- Q7
create or replace function 
    fac(int) returns int
as $$
    select product(val) from seq($1); 
$$ language sql;

create aggregate product(integer) (
    initcond = 1,
    stype = integer,
    sfunc = multipleWith
);

create or replace function
    multipleWith(integer, integer) returns integer
as $$
declare
    x alias for $1;
    y alias for $2;
begin
    return x * y;
end;
$$ language plpgsql;

-- q8
create or replace function
    hotelsIn(loca text) returns text
as $$
declare
    r record;
    res text := '';
begin
    for r in select * from bars where addr = loca loop
        res := res || r.name || '\n';
    end loop;
    return res;
end;
$$ language plpgsql;

-- Q9
create or replace function
    hotelsIn(loca text) returns text
as $$
declare
    pubnames text;
    r record;
begin
    pubnames := 'Hotels in ' || address || ':';
    for r in selet * from Bars where addr = loca
    loop
        pubnames := pubnames||' '||p.name;
    end loop;
    pubnames := pubnames||'\n';
    return pubnames;
end;
$$ language plpgsql;

-- Q10
create or replace function
    hotelsIn(loca text) returns text
as $$
declare
    pubnames text := '';
    r record;
    i integer := 1;
    howmany integer := 0;
begin
    select count(*) into howmany from Bars where addr = loca;
    if (howmany = 0) then
        pubnames := pubnames || 'There are no holets in ' || loca;
    else
        pubnames := pubnames || 'Hotels in ' || loca || '\n';
        for r in select * from Bars where addr = loca
        loop
            pubnames := pubnames || to_char(i, 99) || '. ' || r.name || '\n';
            i := i + 1;
        end loop;
    end if;
    return pubnames;
end;
$$ language plpgsql;

-- Q11
-- Q12

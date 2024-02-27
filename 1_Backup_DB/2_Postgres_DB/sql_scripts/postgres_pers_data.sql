CREATE TABLE pers_data
(user_id varchar(20), 
 name varchar(20),
 age int,
 sex varchar(15),
 username varchar(30),
 date_registration varchar(20)
);

ALTER TABLE pers_data REPLICA IDENTITY FULL;

SELECT * FROM pers_data
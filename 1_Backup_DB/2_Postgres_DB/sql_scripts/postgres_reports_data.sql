CREATE TABLE reports_data
(user_id varchar(20), 
 pari_report varchar,
 date varchar,
 status varchar,
 reason varchar,
 date_waiting varchar
);

ALTER TABLE reports_data REPLICA IDENTITY FULL;

SELECT * FROM reports_data
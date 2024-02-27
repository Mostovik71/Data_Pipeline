CREATE TABLE habit_data
(user_id varchar(20), 
 habit_category varchar,
 habit_choice varchar,
 habit_frequency varchar,
 habit_report varchar,
 habit_mate_sex varchar,
 habit_notification_day varchar,
 habit_notification_time varchar,
 habit_week varchar
);

ALTER TABLE habit_data REPLICA IDENTITY FULL;

SELECT * FROM habit_data

CREATE TABLE habit.clckhs_habit_data 
(
 user_id String, 
 habit_category String,
 habit_choice String,
 habit_frequency String,
 habit_report String,
 habit_mate_sex String,
 habit_notification_day String,
 habit_notification_time String,
 habit_week String
)
ENGINE = MergeTree
PRIMARY KEY (user_id)

CREATE TABLE habit.clckhs_habit_data_kafka 
(
 `after.user_id` String, 
 `after.habit_category` String,
 `after.habit_choice` String, 
 `after.habit_frequency` String,
 `after.habit_report` String, 
 `after.habit_mate_sex` String,
 `after.habit_notification_day` String, 
 `after.habit_notification_time` String,
 `after.habit_week` String
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:9092',
       kafka_topic_list = 'postgres.public.habit_data',
       kafka_group_name = 'group1',
       kafka_format='JSONEachRow';
       
CREATE MATERIALIZED VIEW habit.habit_consumer TO habit.clckhs_habit_data
    AS SELECT 
    	after.user_id as user_id, 
    	after.habit_category as habit_category,
    	after.habit_choice as habit_choice, 
    	after.habit_frequency as habit_frequency,
    	after.habit_report as habit_report, 
    	after.habit_mate_sex as habit_mate_sex,
    	after.habit_notification_day as habit_notification_day, 
    	after.habit_notification_time as habit_notification_time,
    	after.habit_week as habit_week 
    FROM habit.clckhs_habit_data_kafka;
    
select * from habit.clckhs_habit_data
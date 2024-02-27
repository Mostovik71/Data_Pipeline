CREATE TABLE habit.clckhs_pers_data 
(
 user_id String, 
 name String,
 age Int64,
 sex String,
 username String,
 date_registration String
)
ENGINE = MergeTree
PRIMARY KEY (user_id)

CREATE TABLE habit.clckhs_pers_data_kafka 
(
 `after.user_id` String, 
 `after.name` String,
 `after.age` Int64, 
 `after.sex` String,
 `after.username` String, 
 `after.date_registration` String
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:9092',
       kafka_topic_list = 'postgres.public.pers_data',
       kafka_group_name = 'group1',
       kafka_format='JSONEachRow';
       
CREATE MATERIALIZED VIEW habit.pers_consumer TO habit.clckhs_pers_data
    AS SELECT 
    	after.user_id as user_id, 
    	after.name as name,
    	after.age as age, 
    	after.sex as sex,
    	after.username as username, 
    	after.date_registration as date_registration
    FROM habit.clckhs_pers_data_kafka;
    
select * from habit.clckhs_pers_data


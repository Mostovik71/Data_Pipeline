CREATE TABLE habit.clckhs_reports_data 
(
 user_id String, 
 pari_report String,
 date String,
 status String,
 reason String,
 date_waiting String
)
ENGINE = MergeTree
PRIMARY KEY (user_id)


CREATE TABLE habit.clckhs_reports_data_kafka 
(
 user_id String, 
 pari_report String,
 date String,
 status String,
 reason String,
 date_waiting String
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:9092',
       kafka_topic_list = 'postgres.public.reports_data',
       kafka_group_name = 'group1',
       kafka_format='JSONEachRow';
       

 CREATE MATERIALIZED VIEW habit.consumer TO habit.clckhs_reports_data
    AS SELECT user_id, pari_report, date, status, reason, date_waiting
    FROM habit.clckhs_reports_data_kafka;
   
   
SELECT *
FROM habit.clckhs_reports_data
      
      
      
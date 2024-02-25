CREATE TABLE habit.clckhs_reports_data 
(
 user_id String, 
 pari_report String
)
ENGINE = MergeTree
PRIMARY KEY (user_id)

CREATE TABLE habit.clckhs_reports_data_kafka 
(
 `after.user_id` String, 
 `after.pari_report` String
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:9092',
       kafka_topic_list = 'postgres.public.reports_data',
       kafka_group_name = 'group1',
       kafka_format='JSONEachRow';
       
CREATE MATERIALIZED VIEW habit.consumer TO habit.clckhs_reports_data
    AS SELECT after.user_id as user_id, after.pari_report as pari_report
    FROM habit.clckhs_reports_data_kafka;
    
select * from habit.clckhs_reports_data
      
      
      
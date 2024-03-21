from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
import pyspark.sql.functions as F
import clickhouse_connect

import os
 
os.environ["JAVA_HOME"] = 'C:\Program Files\Java\jdk-17'
os.environ["SPARK_HOME"] = 'C:\Program Files\ApacheSpark\spark-3.4.2-bin-hadoop3'
os.environ["HADOOP_HOME"] = 'C:\Program Files\ApacheSpark\spark-3.4.2-bin-hadoop3'
clickhouse_driver_path = "C:/Program Files/ApacheSpark/spark-3.4.2-bin-hadoop3/jars/clickhouse-jdbc-0.4.6.jar"


# Создаем объект SparkSession
spark = SparkSession.builder.master('local[*]')\
                            .config("spark.driver.extraClassPath", clickhouse_driver_path)\
                            .getOrCreate()

habit_schema = StructType([ 
    StructField('user_id', StringType(), True), 
    StructField('habit_category', StringType(), True), 
    StructField('habit_choice', StringType(), True), 
    StructField('habit_frequency', StringType(), True), 
    StructField('habit_report', StringType(), True),
    StructField('habit_mate_sex', StringType(), True), 
    StructField('habit_notification_day', StringType(), True), 
    StructField('habit_notification_time', StringType(), True),
    StructField('habit_week', StringType(), True),
]) 

# Записываем агрегированные данные в ClickHouse

main_database_name = 'habit'
main_table_name = 'clckhs_habit_data'

sdf_habit = spark.read\
    .format("jdbc")\
    .schema(habit_schema)\
    .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")\
    .option("url", "jdbc:clickhouse://127.0.0.1:8123")\
    .option('dbtable', f'{main_database_name}.{main_table_name}')\
    .option("user", "admin")\
    .option("password", "root")\
    .load()


group_action = 'count'

sdf_habit_category_group = sdf_habit.groupby('habit_category').count()
sdf_habit_choice_group = sdf_habit.groupby('habit_choice').count()
sdf_habit_sex_group = sdf_habit.groupby('habit_mate_sex').count()
sdf_habit_notification_day_group = sdf_habit.select(F.col('user_id'), F.explode(F.from_json(F.col('habit_notification_day'), ArrayType(StringType(), True))).alias('notification_day'))\
                                            .groupby('notification_day').count()
sdf_habit_notification_time_group = sdf_habit.select(F.col('user_id'), F.explode(F.from_json(F.col('habit_notification_time'), ArrayType(StringType(), True))).alias('notification_time'))\
                                             .groupby('notification_time').count()

sdfs = {'habit_category_group': sdf_habit_category_group,
        'habit_choice_group': sdf_habit_choice_group,
        'habit_sex_group': sdf_habit_sex_group,
        'habit_notification_day_group': sdf_habit_notification_day_group,
        'habit_notification_time_group': sdf_habit_notification_time_group}

### ClickHouse interacting

client = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='root')

db_name = 'pers_data_aggregate'

clckhs_database_drop = f'DROP DATABASE IF EXISTS {db_name}'
clckhs_database_create = f'CREATE DATABASE IF NOT EXISTS {db_name}'

client.command(clckhs_database_drop)
client.command(clckhs_database_create)

for sdf_name, sdf in sdfs.items():

    clckhs_attributes = dict(sdf.dtypes)

    clckhs_table_name = f'{sdf_name}_table'
    clckhs_table_columns = ', '.join(f'{key} {value.capitalize()}' for key, value in clckhs_attributes.items())
    primary_key = list(clckhs_attributes.keys())[0]

    clckhs_table_drop_query = f'''
        DROP TABLE IF EXISTS {db_name}.{clckhs_table_name} 
    '''
    clckhs_table_creation_query = f'''
        CREATE TABLE {db_name}.{clckhs_table_name} 
        ( 
        {clckhs_table_columns}
        )
        ENGINE = Log
    '''
    client.command(clckhs_table_drop_query)
    client.command(clckhs_table_creation_query)

    sdf.orderBy(group_action, ascending=False).write\
        .format("jdbc")\
        .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")\
        .option("url", "jdbc:clickhouse://127.0.0.1:8123")\
        .option("user", "admin")\
        .option("password", "root")\
        .option('dbtable', f'{db_name}.{clckhs_table_name}').save(mode='append')

spark.stop()


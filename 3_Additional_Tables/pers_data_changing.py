from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType
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

pers_schema = StructType([ 
    StructField('user_id', StringType(), True), 
    StructField('name', StringType(), True), 
    StructField('age', LongType(), True), 
    StructField('sex', StringType(), True), 
    StructField('username', StringType(), True),
    StructField('date_registration', StringType(), True)
]) 

# Записываем агрегированные данные в ClickHouse

main_database_name = 'habit'
main_table_name = 'clckhs_pers_data'

sdf_pers = spark.read\
    .format("jdbc")\
    .schema(pers_schema)\
    .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")\
    .option("url", "jdbc:clickhouse://127.0.0.1:8123")\
    .option('dbtable', f'{main_database_name}.{main_table_name}')\
    .option("user", "admin")\
    .option("password", "root")\
    .load()

sdf_pers = sdf_pers.withColumn('age_part', F.when(F.col('age').between(0, 18), '0 - 18')\
                                            .when(F.col('age').between(19, 30), '19 - 30')\
                                            .when(F.col('age').between(31, 40), '31 - 40')\
                                            .when(F.col('age').between(41, 60), '41 - 60')\
                                            .when(F.col('age').between(61, 80), '61 - 80')\
                                            .when(F.col('age').between(81, 100), '81 - 100')\
                                            .otherwise('Very old people'))

group_action = 'count'

sdf_pers_sex_group = sdf_pers.groupby('sex').count()
sdf_pers_age_group = sdf_pers.groupby('age').count()    
sdf_pers_age_part_group = sdf_pers.groupby('age_part').count()                  


sdfs = {'pers_sex_group': sdf_pers_sex_group,
        'pers_age_group': sdf_pers_age_group,
        'pers_age_part_group': sdf_pers_age_part_group}

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

    sdf.orderBy('count', ascending=False).write\
        .format("jdbc")\
        .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")\
        .option("url", "jdbc:clickhouse://127.0.0.1:8123")\
        .option("user", "admin")\
        .option("password", "root")\
        .option('dbtable', f'{db_name}.{clckhs_table_name}').save(mode='append')

spark.stop()


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

report_schema = StructType([ 
    StructField('user_id', StringType(), True), 
    StructField('pari_report', StringType(), True), 
    StructField('date', StringType(), True), 
    StructField('status', StringType(), True), 
    StructField('reason', StringType(), True),
    StructField('date_waiting', StringType(), True)
]) 

# Записываем агрегированные данные в ClickHouse

main_database_name = 'habit'
main_table_name = 'clckhs_reports_data'

sdf_report = spark.read\
    .format("jdbc")\
    .schema(report_schema)\
    .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")\
    .option("url", "jdbc:clickhouse://127.0.0.1:8123")\
    .option('dbtable', f'{main_database_name}.{main_table_name}')\
    .option("user", "admin")\
    .option("password", "root")\
    .load()


group_action = 'count'

sdf_report_pari_report_pivot = sdf_report.groupby('user_id').pivot('pari_report').count()\
                                         .fillna(0)
sdf_report_pari_report_pivot = sdf_report_pari_report_pivot.withColumn('total_amount', sum(sdf_report_pari_report_pivot[x] for x in sdf_report_pari_report_pivot.columns[1:]))

sdf_report_status_pivot = sdf_report.groupby('user_id').pivot('status').count()\
                                    .fillna(0)
sdf_report_status_pivot = sdf_report_status_pivot.withColumn('total_amount', sum(sdf_report_status_pivot[x] for x in sdf_report_status_pivot.columns[1:]))
    
                                    


sdfs = {'report_pari_report_pivot': sdf_report_pari_report_pivot,
        'report_status_pivot': sdf_report_status_pivot}

### ClickHouse interacting

client = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='root')

db_name = 'report_data_aggregate'

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

    sdf.write\
        .format("jdbc")\
        .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")\
        .option("url", "jdbc:clickhouse://127.0.0.1:8123")\
        .option("user", "admin")\
        .option("password", "root")\
        .option('dbtable', f'{db_name}.{clckhs_table_name}').save(mode='append')

spark.stop()


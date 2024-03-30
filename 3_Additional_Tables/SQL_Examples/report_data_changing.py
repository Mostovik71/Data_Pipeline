import clickhouse_connect

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta


def pivot_func(main_database_name, main_table_name, new_database_name, new_table_name, pivot_col_name, group_agg_name, values_list):

    queries = [f"{group_agg_name}(case when {pivot_col_name} = '{value}' then {pivot_col_name} end) as {value}" for value in values_list]

    pivot_query = f'''
                    CREATE TABLE {new_database_name}.{new_table_name} 
                    ENGINE = Log 
                    AS 
                    (select user_id, 
                                {', '.join(queries)},
                                {group_agg_name}({pivot_col_name}) as total
                            from {main_database_name}.{main_table_name} 
                            group by user_id)
                    '''
    
    return pivot_query


def get_connection(host, port, username, password):
    connection = clickhouse_connect.get_client(host=host, port=port, username=username, password=password)

    return connection


### DAG Tasks

def print_dag_start():
    print('This is the DAG for reports_table')


def commands_task():
    
    pivot_query_1 = pivot_func(
                           main_database_name='habit', 
                           main_table_name='clckhs_reports_data', 
                           new_database_name='report_agg',
                           new_table_name='pari_report_agg',
                           pivot_col_name='pari_report',
                           group_agg_name='count',
                           values_list=['photo', 'video_note', 'text']
                           )

    pivot_query_2 = pivot_func(
                           main_database_name='habit', 
                           main_table_name='clckhs_reports_data', 
                           new_database_name='report_agg',
                           new_table_name='status_agg',
                           pivot_col_name='status',
                           group_agg_name='count',
                           values_list=['approved', 'waiting', 'rejected', 'deleted']
                           )

    clckhs_database_drop = 'DROP DATABASE IF EXISTS report_agg'
    clckhs_database_create = 'CREATE DATABASE IF NOT EXISTS report_agg'

    client = get_connection(host='host.docker.internal',
                            port=8123,
                            username='admin',
                            password='root')


    client.command(clckhs_database_drop)
    client.command(clckhs_database_create)


    client.command(pivot_query_1)
    client.command(pivot_query_2)
 

dag = DAG(
    'report_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval=timedelta(minutes=2),
    catchup=False
)

dag_start_task = PythonOperator(
    task_id='report_dag_start',
    python_callable=print_dag_start,
    dag=dag
)

report_insert_task = PythonOperator(
    task_id='report_commands',
    python_callable=commands_task,
    dag=dag
)

dag_start_task >> report_insert_task


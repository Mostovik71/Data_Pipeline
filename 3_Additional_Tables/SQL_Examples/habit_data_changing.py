import clickhouse_connect

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta


def group_func(main_database_name, main_table_name, new_database_name, new_table_name, group_col_name, group_agg_name):

    group_query = f'''
                    CREATE TABLE {new_database_name}.{new_table_name} 
                    ENGINE = Log 
                    AS 
                    (SELECT {group_col_name}, {group_agg_name}({group_col_name}) as {group_agg_name}
                    FROM {main_database_name}.{main_table_name}
                    GROUP BY {group_col_name} ORDER BY {group_agg_name} DESC)
                    '''
    
    return group_query

def explode_group_func(main_database_name, main_table_name, new_database_name, new_table_name, group_col_name, group_agg_name):

    explode_group_query = f'''
                    CREATE TABLE {new_database_name}.{new_table_name} 
                    ENGINE = Log 
                    AS 
                    (select trimLeft(tms) as {group_col_name}, count(tms) as count from 
                        (select user_id, splitByChar(',', trim(BOTH '[]' FROM {group_col_name})) as tm from {main_database_name}.{main_table_name}) 
                        ARRAY JOIN tm as tms
                        GROUP BY trimLeft(tms) ORDER BY {group_agg_name} DESC)
                    '''
    
    return explode_group_query

def get_connection(host, port, username, password):
    connection = clickhouse_connect.get_client(host=host, port=port, username=username, password=password)

    return connection


### DAG Tasks

def print_dag_start():
    print('This is the DAG for habit_table')


def commands_task():
    
    group_query_1 = group_func(
                           main_database_name='habit', 
                           main_table_name='clckhs_habit_data', 
                           new_database_name='habit_agg',
                           new_table_name='habit_category_agg',
                           group_col_name='habit_category',
                           group_agg_name='count'
                           )

    group_query_2 = group_func(
                            main_database_name='habit', 
                            main_table_name='clckhs_habit_data', 
                            new_database_name='habit_agg',
                            new_table_name='habit_choice_agg',
                            group_col_name='habit_choice',
                            group_agg_name='count'
                            )

    group_query_3 = group_func(
                            main_database_name='habit', 
                            main_table_name='clckhs_habit_data', 
                            new_database_name='habit_agg',
                            new_table_name='habit_mate_sex_agg',
                            group_col_name='habit_mate_sex',
                            group_agg_name='count'
                            )

    explode_group_query_1 = explode_group_func(
                                                main_database_name='habit', 
                                                main_table_name='clckhs_habit_data', 
                                                new_database_name='habit_agg',
                                                new_table_name='habit_notification_time_agg',
                                                group_col_name='habit_notification_time',
                                                group_agg_name='count'
                                                )

    explode_group_query_2 = explode_group_func(
                                                main_database_name='habit', 
                                                main_table_name='clckhs_habit_data', 
                                                new_database_name='habit_agg',
                                                new_table_name='habit_notification_day_agg',
                                                group_col_name='habit_notification_day',
                                                group_agg_name='count'
                                                )

    clckhs_database_drop = 'DROP DATABASE IF EXISTS habit_agg'
    clckhs_database_create = 'CREATE DATABASE IF NOT EXISTS habit_agg'

    client = get_connection(host='host.docker.internal',
                            port=8123,
                            username='admin',
                            password='root')


    client.command(clckhs_database_drop)
    client.command(clckhs_database_create)


    client.command(group_query_1)
    client.command(group_query_2)
    client.command(group_query_3)

    client.command(explode_group_query_1)
    client.command(explode_group_query_2)

dag = DAG(
    'habit_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval=timedelta(minutes=2),
    catchup=False
)

dag_start_task = PythonOperator(
    task_id='habit_dag_start',
    python_callable=print_dag_start,
    dag=dag
)

habit_insert_task = PythonOperator(
    task_id='habit_commands',
    python_callable=commands_task,
    dag=dag
)

dag_start_task >> habit_insert_task


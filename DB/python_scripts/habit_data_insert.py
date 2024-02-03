import pandas as pd
import psycopg2
conn = psycopg2.connect(dbname='postgres', user='admin', 
                        password='root', host='localhost')
cursor = conn.cursor()

habit_data = pd.read_csv('Data/habit_data_upd.csv')
habit_data.habit_notification_day = habit_data.habit_notification_day.str.replace("'", '"')
habit_data.habit_notification_time = habit_data.habit_notification_time.str.replace("'", '"')
for i in habit_data.iterrows():
    insert = f'''
                INSERT INTO 
                habit_data (user_id, habit_category, habit_choice, habit_frequency, habit_report, habit_mate_sex, habit_notification_day, habit_notification_time, habit_week) 
                VALUES ('{i[1]['user_id']}', 
                        '{i[1]['habit_category']}', 
                        '{i[1]['habit_choice']}', 
                        '{i[1]['habit_frequency']}', 
                        '{i[1]['habit_report']}', 
                        '{i[1]['habit_mate_sex']}',
                        '{i[1]['habit_notification_day']}',
                        '{i[1]['habit_notification_time']}',
                        '{i[1]['habit_week']}'
                        )
             '''
    cursor.execute(insert)
conn.commit()


# cursor.execute('select * from pers_data')
# records = cursor.fetchall()
# print(records)

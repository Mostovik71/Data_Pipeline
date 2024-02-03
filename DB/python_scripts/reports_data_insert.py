import pandas as pd
import psycopg2
conn = psycopg2.connect(dbname='postgres', user='admin', 
                        password='root', host='localhost')
cursor = conn.cursor()

habit_data = pd.read_csv('Data/reports_data_upd.csv')
for i in habit_data.iterrows():
    insert = f'''
                INSERT INTO 
                reports_data (user_id, pari_report, date, status, reason, date_waiting) 
                VALUES ('{i[1]['user_id']}', 
                        '{i[1]['pari_report']}', 
                        '{i[1]['date']}', 
                        '{i[1]['status']}', 
                        '{i[1]['reason']}', 
                        '{i[1]['date_waiting']}')
             '''
    cursor.execute(insert)
conn.commit()
import pandas as pd
import psycopg2
conn = psycopg2.connect(dbname='habit', user='admin', 
                        password='root', host='localhost')
cursor = conn.cursor()

habit_data = pd.read_csv('Data/pers_data_upd.csv')
for i in habit_data.iterrows():
    insert = f'''
                INSERT INTO 
                pers_data (user_id, name, age, sex, username, date_registration) 
                VALUES ('{i[1]['user_id']}', '{i[1]['name']}', {i[1]['age']}, '{i[1]['sex']}', '{i[1]['username']}', '{i[1]['date_registration']}')
             '''
    cursor.execute(insert)
conn.commit()


# cursor.execute('select * from pers_data')
# records = cursor.fetchall()
# print(records)

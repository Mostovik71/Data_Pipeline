import psycopg2
conn = psycopg2.connect(dbname='habit', user='admin', 
                        password='root', host='localhost')
cursor = conn.cursor()
cursor.execute('SELECT * FROM habit_data LIMIT 10')
records = cursor.fetchall()
print(records)
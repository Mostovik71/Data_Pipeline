import psycopg2
conn = psycopg2.connect(dbname='postgres', user='admin', 
                        password='root', host='localhost')
cursor = conn.cursor()
cursor.execute('SELECT * FROM customers LIMIT 10')
records = cursor.fetchall()
print(records)
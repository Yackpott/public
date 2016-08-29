import psycopg2

conn = psycopg2.connect("dbname=cookies")
cursor = conn.cursor()
cursor.execute("select host_key from cookies limit 10")
results = cursor.fetchall()
print(results)
conn.commit()
conn.close()

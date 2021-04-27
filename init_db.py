import psycopg2

conn = psycopg2.connect(
    database="postgres", user='postgres', password='password', host='localhost', port='5432'
)
conn.autocommit = True
statements = ['''CREATE database pw_db;''',
              '''CREATE USER pw_user with password '123456';''',
              '''GRANT ALL PRIVILEGES ON DATABASE pw_db to pw_user;''']
cursor = conn.cursor()

for state in statements:
    cursor.execute(state)

conn.close()

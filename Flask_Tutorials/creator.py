from user import User
import psycopg2

connection = psycopg2.connect(host='localhost',
                              database='postgres',
                              port=5432,
                              user='postgres',
                              password='1111')

user = User(1, 'user', 'User Name')
user.set_password('password')
cursor = connection.cursor()
cursor.execute(f'INSERT INTO users(username, name, password_hash) VALUES(%s, %s, %s)', (user.username, user.name, user.password_hash))
print('added')
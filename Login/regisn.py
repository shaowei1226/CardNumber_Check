from werkzeug.security import generate_password_hash
import pymysql

# 假設使用者資料
username = 'new_user'
password = 'secure_password'
hashed_password = generate_password_hash(password)

db_host = 'localhost'
db_user = 'root'
db_password = '120129'
db_name = 'card_database'
db_port = 3300

def connect_db():
    try:
        conn = pymysql.connect(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name, 
            port=db_port
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None


conn = connect_db()
cursor = conn.cursor()

cursor.execute('INSERT INTO users (username, password, card_number) VALUES (%s, %s, %s)', 
               (username, hashed_password, '1234567890123456'))

conn.commit()
conn.close()

from flask import Flask, request, redirect, url_for, render_template
import pymysql
from werkzeug.security import check_password_hash

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = connect_db()
    if conn is None:
        return "Database connection failed", 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return "Database query failed", 500
    finally:
        conn.close()
    
    if user and check_password_hash(user['password'], password):
        return redirect(url_for('card_system', card_number=user['card_number']))
    else:
        return 'Login Failed'

@app.route('/card_system')
def card_system():
    card_number = request.args.get('card_number')
    return redirect(f'http://127.0.0.1:5000')

if __name__ == "__main__":
    app.run(debug=True,port=5002)

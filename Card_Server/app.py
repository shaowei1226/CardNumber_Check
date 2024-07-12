from flask import Flask, request, render_template , jsonify ,redirect , url_for
import pymysql
import datetime
import string
import random 
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# MySQL資料庫連接設置
db_host = 'localhost'
db_user = 'root'
db_password = '120129'
db_name = 'card_database'
db_port = 3300

def connect_db():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)

@app.route('/')
def home():
    return render_template('login.html')
#####login_API#########
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
        return redirect(f'http://127.0.0.1:5000/card_system')
    else:
        return 'Login Failed'
    
    
#####註冊頁面#########
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect_db()
        if conn is None:
            return "Database connection failed", 500

        try:
            # 檢查用戶是否已經存在
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                return "使用者名稱重複註冊"

            # 如果用戶不存在，則將用戶添加到資料庫
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()

            return render_template('login.html')

        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            return "Database query failed", 500
        finally:
            conn.close()

    return render_template('login.html')
####產生卡號#######
@app.route('/card_system', methods=['GET', 'POST'])
def index():
    card_number = None
    if request.method == 'POST':
        expiry_minutes = int(request.form['expiry'])
        expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes)
        card_number = generate_card_number()
        
        conn = connect_db()
        cursor = conn.cursor()
        
        sql = "INSERT INTO card (card_number, expiry_time) VALUES (%s, %s)"
        cursor.execute(sql, (card_number, expiry_time))
        conn.commit()
        
        cursor.close()
        conn.close()

    return render_template('index.html', card_number=card_number)
###卡號驗證#####
@app.route('/verify_card', methods=['POST'])
def verify_card():
    data = request.get_json()
    card_number = data.get('card_number')
    machine_code = data.get('machine_code')
    
    

    conn = connect_db()
    cursor = conn.cursor()
    cursor_first =conn.cursor()
    
    print(f"Received card_number: {card_number}")
    print(f"Received machine_code: {machine_code}")
    #第一次登入卡號
    sql_first = "SELECT expiry_time FROM card WHERE card_number = %s"
    cursor_first.execute(sql_first, (card_number,))
    result = cursor_first.fetchone()

    
    #卡號已經登入過後的SQL語法
    ##sql = "SELECT expiry_time,machinecode FROM card WHERE card_number = %s and machinecode = %s"
  
    ##cursor.execute(sql, (card_number,machine_code))
    
    ##result = cursor.fetchone()
    
    if result :
        sql_update_query = "UPDATE card SET machinecode = %s WHERE card_number = %s"
        cursor.execute(sql_update_query, (machine_code, card_number))
        conn.commit() 
    else:
        print ("Errorcode:machinecode")
    
    cursor.close()
    conn.close()

    if result:
        expiry_time = result[0]
        if expiry_time > datetime.datetime.now():
            
            return jsonify({'status': 'success', 'message': '卡號驗證成功！歡迎進入系統。'})
            
        else:
            return jsonify({'status': 'error', 'message': '卡號已過期！'})
    else:
        return jsonify({'status': 'error', 'message': '卡號不存在或無效！請重新輸入。'})
    
def generate_card_number():
    # 定义字符集，包括大写字母、小写字母和数字
    characters = string.ascii_letters + string.digits
    # 生成12位随机字符串
    random_string = ''.join(random.choices(characters, k=12))
    return random_string

if __name__ == '__main__':
    app.run(debug=True)

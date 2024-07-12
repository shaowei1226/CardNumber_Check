from flask import Flask, request, render_template , jsonify
import pymysql
import datetime
import string
import random 

app = Flask(__name__)

# MySQL資料庫連接設置
db_host = 'localhost'
db_user = 'root'
db_password = '120129'
db_name = 'card_database'
db_port = 3300

def connect_db():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)

@app.route('/', methods=['GET', 'POST'])
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

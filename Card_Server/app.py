from flask import Flask, render_template, request
import pymysql
import secrets

app = Flask(__name__)

# MySQL資料庫連接設置
db_host = 'localhost'
db_user = 'root'  # 使用者名稱
db_password = '120129'  # 密碼
db_name = 'card_database'  # 資料庫名稱
db_port = 3300  # 埠號

# 連接到MySQL資料庫
def connect_db():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)

# 生成隨機卡號
def generate_card_number():
    return secrets.token_hex(16)  # 生成一個16位的隨機十六進制數字

@app.route('/', methods=['GET', 'POST'])
def index():
    card_number = None

    if request.method == 'POST':
        # 生成卡號並保存到資料庫
        card_number = generate_card_number()

        conn = connect_db()
        cursor = conn.cursor()

        # 插入卡號到資料庫
        sql = "INSERT INTO card (card_number) VALUES (%s)"
        cursor.execute(sql, (card_number,))
        conn.commit()

        cursor.close()
        conn.close()

    return render_template('index.html', card_number=card_number)

if __name__ == '__main__':
    app.run(debug=True)

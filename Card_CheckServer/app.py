from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# MySQL資料庫連接設置
db_host = 'localhost'
db_user = 'root'  # 使用者名稱
db_password = '120129'  # 密碼
db_name = 'card_database'  # 資料庫名稱
db_port = 3300  # 埠號

# 連接到MySQL資料庫
def connect_db():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)

@app.route('/verify_card', methods=['POST'])
def verify_card():
    data = request.get_json()
    card_number = data.get('card_number')

    conn = connect_db()
    cursor = conn.cursor()

    # 檢查卡號是否存在於資料庫中
    sql = "SELECT * FROM card WHERE card_number = %s"
    cursor.execute(sql, (card_number,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return jsonify({'status': 'success', 'message': '卡號驗證成功！歡迎進入系統。'})
    else:
        return jsonify({'status': 'error', 'message': '卡號不存在或無效！請重新輸入。'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 伺服器在5001端口運行

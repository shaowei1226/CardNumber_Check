from flask import Flask, request, render_template
import pymysql
import datetime

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

def generate_card_number():
    # 生成一個唯一的卡號，例如使用UUID
    import uuid
    return str(uuid.uuid4())

if __name__ == '__main__':
    app.run(debug=True)

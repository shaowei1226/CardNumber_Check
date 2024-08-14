import tkinter as tk
import sqlite3
from tkinter import messagebox
import pymysql

db_host = 'localhost'
db_user = 'root'
db_password = '120129'
db_name = 'card_database'
db_port = 3300

def connect_db():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)

def open_poker_hand_gui():
    poker_root = tk.Tk()
    poker_root.title("撲克手牌紀錄")

    # 定義欄位標籤及輸入框
    labels = [
        "Level", 
        "玩家人數", 
        "Hero 位置", 
        "Hero 後手", 
        "其他玩家後手",
        "Hero 手牌", 
        "翻前Action", 
        "Flop 開的牌", 
        "Flop Action", 
        "Turn 開的牌", 
        "Turn Action", 
        "River 開的牌", 
        "River Action"
    ]
    
    entries = {}

    for i, label_text in enumerate(labels):
        label = tk.Label(poker_root, text=label_text + ":")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        
        entry = tk.Entry(poker_root, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
        entries[label_text] = entry

    # 保存按鈕
    save_button = tk.Button(poker_root, text="保存手牌記錄", command=lambda: save_hand_record(entries))
    save_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

    poker_root.mainloop()

def save_hand_record(entries):
    hand_data = {key: entry.get() for key, entry in entries.items()}

    # 連接資料庫
    conn = connect_db()
    cursor = conn.cursor()

    # 將手牌記錄插入資料庫
    cursor.execute('''
        INSERT INTO poker_hands (
            level, 
            player_count, 
            hero_position, 
            hero_stack, 
            other_player_stacks, 
            hero_hand, 
            preflop_action, 
            flop_cards, 
            flop_action, 
            turn_card, 
            turn_action, 
            river_card, 
            river_action
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        hand_data["Level"],
        hand_data["玩家人數"],
        hand_data["Hero 位置"],
        hand_data["Hero 後手"],
        hand_data["其他玩家後手"],
        hand_data["Hero 手牌"],
        hand_data["翻前Action"],
        hand_data["Flop 開的牌"],
        hand_data["Flop Action"],
        hand_data["Turn 開的牌"],
        hand_data["Turn Action"],
        hand_data["River 開的牌"],
        hand_data["River Action"]
    ))

    conn.commit()
    conn.close()

    # 顯示保存成功訊息
    messagebox.showinfo("保存成功", "手牌記錄已保存到資料庫！")

if __name__ == "__main__":
    open_poker_hand_gui()

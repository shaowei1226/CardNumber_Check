import tkinter as tk
from tkinter import messagebox
import requests
import os

# API 伺服器 URL
API_URL = 'http://localhost:5001/verify_card'
# 卡號文件
CARD_FILE = 'card_number.txt'

def load_card_number():
    """從文件加載卡號"""
    if os.path.exists(CARD_FILE):
        with open(CARD_FILE, 'r') as file:
            return file.read().strip()
    return ''

def save_card_number(card_number):
    """保存卡號到文件"""
    with open(CARD_FILE, 'w') as file:
        file.write(card_number)

def verify_card():
    card_number = card_entry.get()

    if not card_number:
        messagebox.showerror("Error", "請輸入卡號！")
        return

    # 發送 POST 請求到 API
    response = requests.post(API_URL, json={'card_number': card_number})

    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'success':
            save_card_number(card_number)
            messagebox.showinfo("Success", result['message'])
        else:
            messagebox.showerror("Error", result['message'])
    else:
        messagebox.showerror("Error", "無法連接到伺服器！")

# 建立主視窗
root = tk.Tk()
root.title("卡號驗證系統")

# 建立元件
card_label = tk.Label(root, text="輸入卡號:")
card_label.pack(pady=10)

# 預設卡號
default_card_number = load_card_number()
card_entry = tk.Entry(root, width=30)
card_entry.insert(0, default_card_number)
card_entry.pack()

verify_button = tk.Button(root, text="驗證卡號", command=verify_card)
verify_button.pack(pady=10)

# 執行主迴圈
root.mainloop()

# gui/login_window.py

import tkinter as tk
from tkinter import messagebox
import sqlite3
from gui.dashboard import open_dashboard

def show_login_window():
    def login():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("db/inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            root.destroy()
            open_dashboard(role, username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    root = tk.Tk()
    root.title("Inventory App Login")
    root.geometry("300x200")

    tk.Label(root, text="Username").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Button(root, text="Login", command=login).pack(pady=20)

    root.mainloop()

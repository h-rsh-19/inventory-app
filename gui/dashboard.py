# gui/dashboard.py
from gui.add_product_window import open_add_product_window
import tkinter as tk
from tkinter import messagebox
from gui.manage_products_window import open_manage_products


def open_dashboard(role, username):
    window = tk.Tk()
    window.title(f"{role.capitalize()} Dashboard - Welcome {username}")
    window.geometry("400x300")

    tk.Label(window, text=f"Welcome {username} ({role})", font=("Arial", 14)).pack(pady=20)

    if role == "admin":
        tk.Button(window, text="View Reports", width=25).pack(pady=5)
        tk.Button(window, text="Manage Users", width=25).pack(pady=5)
        tk.Button(window, text="Add New Product", width=25, command=open_add_product_window).pack(pady=5)
        tk.Button(window, text="Manage Products", width=25, command=open_manage_products).pack(pady=5)


    elif role == "billing":
        from gui.billing_window import open_billing_window
        tk.Button(window, text="New Sale (Billing)", width=25, command=lambda: open_billing_window(username)).pack(pady=5)
        tk.Button(window, text="Print Invoice", width=25).pack(pady=5)
        

    elif role == "inventory":
        tk.Button(window, text="Low Stock Alerts", width=25).pack(pady=5)
        tk.Button(window, text="Add New Product", width=25, command=open_add_product_window).pack(pady=5)
        tk.Button(window, text="Manage Products", width=25, command=open_manage_products).pack(pady=5)


    else:
        messagebox.showerror("Error", "Invalid user role.")

    tk.Button(window, text="Logout", command=window.destroy, width=25, fg="red").pack(pady=20)

    window.mainloop()

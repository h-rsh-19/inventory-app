# main.py

from modules.db_init import init_db
from gui.login_window import show_login_window

if __name__ == "__main__":
    init_db()
    show_login_window()

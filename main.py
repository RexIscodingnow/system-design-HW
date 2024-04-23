import os
import time
import bcrypt
import pathlib
import access_db
import tkinter as tk

from config import *
from tkinter import messagebox
from base_window import BaseWindow, all_widgets_map



class Login_SignUp_Window(BaseWindow, tk.Toplevel):
    def __init__(self):
        super().__init__(
            win_title = "用戶登入 / 註冊",
            height = 300
        )

        self.resizable(False, False)
        self.centerToScreen()
        
        # ==============================================================

        """ 輸入框顯示訊息 """

        PLACEHOLDER_EMAIL = "輸入電子信箱"
        PLACEHOLDER_USERNAME = "輸入使用者名稱"
        PLACEHOLDER_PASSWORD = "輸入密碼"

        # ==============================================================

        """ 所有元件設置 """

        lbl_title = tk.Label(self, font=FONT_TEXT, text="登入帳號")
        self.entry_email = tk.Entry(self, font=FONT_ENTRY)
        self.entry_username = tk.Entry(self, font=FONT_ENTRY)
        self.entry_password = tk.Entry(self, font=FONT_ENTRY, name="entry-pwd")
        self.submit_btn = tk.Button(self, font=FONT_BTN, text="登入")
        self.register_btn = tk.Button(self, font=FONT_BTN, text="註冊")


        lbl_title.place(
            x = self.winfo_width() + 190,    y =  10
        )
        self.entry_email.place(
            x = self.winfo_width() + 100,    y =  80
        )
        self.entry_username.place(
            x = self.winfo_width() + 100,    y = 130
        )
        self.entry_password.place(
            x = self.winfo_width() + 100,    y = 180
        )
        self.submit_btn.place(
            x = self.winfo_width() + 160,    y = 230
        )
        self.register_btn.place(
            x = self.winfo_width() + 260,    y = 230
        )

        self.entry_email.insert(0, PLACEHOLDER_EMAIL)
        self.entry_email.configure(state='disabled')
        self.entry_username.insert(0, PLACEHOLDER_USERNAME)
        self.entry_username.configure(state='disabled')
        self.entry_password.insert(0, PLACEHOLDER_PASSWORD)
        self.entry_password.configure(state='disabled')


        # ---------------------------------------------------------

        # 滑鼠左鍵點擊: 消除顯示訊息
        self.entry_email.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_email))
        self.entry_username.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_username))
        self.entry_password.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_password))
        
        # ---------------------------------------------------------
        
        # 離開目標輸入框: 重新顯示訊息
        self.entry_email.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_email, PLACEHOLDER_EMAIL))
        self.entry_username.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_username, PLACEHOLDER_USERNAME))
        self.entry_password.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_password, PLACEHOLDER_PASSWORD))


    def register_user(self):
        __email = self.entry_email.get()
        __username = self.entry_username.get()
        __password = self.entry_password.get()

        # TODO: bcrypt


    def login_user(self):
        pass


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__(
            win_title="Main window",
            height=700
        )
        
        self.centerToScreen()
        self.after(1000, self.open_login_window)


    def open_login_window(self):
        login_window = Login_SignUp_Window()
        login_window.grab_set()



if __name__ == "__main__":
    table_create = """
                    CREATE TABLE IF NOT EXISTS `users` (
                            `id`          INTEGER         PRIMARY KEY     AUTOINCREMENT,
                            `email`       VARCHAR(100)    UNIQUE          NOT NULL,
                            `username`    VARCHAR(20)     NOT NULL,
                            `password`    VARCHAR(20)     NOT NULL,
                            `score`       INTEGER
                    );
                   """
    
    access_db.exec_cmd_sql(table_create)

    # win = MainWindow()
    win = Login_SignUp_Window()


    win.mainloop()


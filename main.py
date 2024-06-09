import os
import re
import time
import bcrypt
import pathlib
import platform
import access_db
import tkinter as tk
import threading as td

# import pygame
import play_tetris_ref as tetris

from config import *
from queue import Queue
from tkinter import messagebox
from base_window import BaseWindow


# TODO: 改架構:
#               1. 登入後 呼叫 tetris.main

def validate_email(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    
    if re.fullmatch(regex, email):
        return True
    else:
        return False


class SignUpWindow(BaseWindow, tk.Toplevel):
    def __init__(self):
        super().__init__("用戶註冊", height=300)

        self.resizable(False, False)
        self.centerToScreen()

        # ==============================================================

        PLACEHOLDER_EMAIL = "輸入電子信箱"
        PLACEHOLDER_USERNAME = "輸入使用者名稱"
        PLACEHOLDER_PASSWORD = "輸入密碼"

        # ==============================================================

        lbl_title = tk.Label(self, font=FONT_TEXT, text="註冊帳號")
        self.entry_email = tk.Entry(self, font=FONT_ENTRY)
        self.entry_username = tk.Entry(self, font=FONT_ENTRY)
        self.entry_password = tk.Entry(self, font=FONT_ENTRY, name="entry-pwd")
        self.register_btn = tk.Button(self, font=FONT_BTN, text="註冊", command=self.register_user)


        lbl_title.place(
            x = 185,    y =  10
        )
        self.entry_email.place(
            x = 100,    y =  80
        )
        self.entry_username.place(
            x = 100,    y = 130
        )
        self.entry_password.place(
            x = 100,    y = 180
        )
        self.register_btn.place(
            x = self.width // 2 - 30,    y = 230
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
        if self.entry_email.cget('state') == 'disabled' or \
            self.entry_username.cget('state') == 'disabled' or \
                self.entry_password.cget('state') == 'disabled':
            return
        
        email = self.entry_email.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if self.entry_email.cget('state') != 'disabled' and not validate_email(email):
            messagebox.showerror("註冊失敗 !", "Email 的格式錯誤 ! 請重新檢查格式是否正確")
            return
        
        # TODO: limit the password min length
        if len(password) < 6:
            messagebox.showinfo("註冊提示 !", "密碼需至少 6 位以上")
            return

        hashed_pwd = bcrypt.hashpw(bytes(password.encode()), bcrypt.gensalt())
        access_db.insert(
            table_name="users",
            params={
                "username": [username],
                "email": [email],
                "password": [hashed_pwd],
                "score": [0],
                "max_lines": [0]
            }
        )

        if "ok" == messagebox.showinfo("註冊", "註冊成功 ! 請關閉註冊視窗 !"):
            self.destroy()


class ForgotPwdWindow(BaseWindow, tk.Toplevel):
    def __init__(self):
        super().__init__(
            win_title = "忘記密碼",
            height = 300
        )

        self.centerToScreen()
        self.resizable(False, False)

        PLACEHOLDER_EMAIL = "輸入電子信箱"
        PLACEHOLDER_PASSWORD = "新密碼"
        PLACEHOLDER_PASSWORD_CONFIRM = "確認密碼"

        lbl_title = tk.Label(self, font=FONT_TEXT, text="重設密碼")
        self.entry_email = tk.Entry(self, font=FONT_ENTRY)
        self.entry_password = tk.Entry(self, font=FONT_ENTRY)
        self.entry_pwd_confirm = tk.Entry(self, font=FONT_ENTRY)
        self.submit_btn = tk.Button(self, font=FONT_BTN, text="送出", command=self.reset_password)
        
        lbl_title.place(
            x = 170,    y =  10
        )
        self.entry_email.place(
            x = 100,    y =  80
        )
        self.entry_password.place(
            x = 100,    y = 130
        )
        self.entry_pwd_confirm.place(
            x = 100,    y = 180
        )
        self.submit_btn.place(
            x = 200,    y = 230
        )

        # ---------------------------------------------------------
        
        self.entry_email.insert(0, PLACEHOLDER_EMAIL)
        self.entry_email.configure(state='disabled')
        self.entry_password.insert(0, PLACEHOLDER_PASSWORD)
        self.entry_password.configure(state='disabled')
        self.entry_pwd_confirm.insert(0, PLACEHOLDER_PASSWORD_CONFIRM)
        self.entry_pwd_confirm.configure(state='disabled')

        # ---------------------------------------------------------

        self.entry_email.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_email))
        self.entry_password.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_password))
        self.entry_pwd_confirm.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_pwd_confirm))
        
        # ---------------------------------------------------------

        self.entry_email.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_email, PLACEHOLDER_EMAIL))
        self.entry_password.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_password, PLACEHOLDER_PASSWORD))
        self.entry_pwd_confirm.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_pwd_confirm, PLACEHOLDER_PASSWORD_CONFIRM))

    
    def reset_password(self):
        if self.entry_email.cget('state') == 'disabled' or \
            self.entry_password.cget('state') == 'disabled' or \
                self.entry_pwd_confirm.cget('state') == 'disabled':
            return
        
        email = self.entry_email.get()
        exist_user, n = access_db.select("users", [("email", email)], ["="])
        print(exist_user, n)

        if n == 0:
            messagebox.showinfo("hint", "查無此帳號 !")
            return
        
        new_password = self.entry_password.get()
        confirm_password = self.entry_pwd_confirm.get()

        if new_password != confirm_password:
            messagebox.showwarning("hint", "密碼必須相同")
            return

        hashed_pwd = bcrypt.hashpw(bytes(new_password.encode()), bcrypt.gensalt())
        access_db.update("users", {
            "email": email,
            "password": hashed_pwd
        })

        if "ok" == messagebox.showinfo("hint", "密碼修改成功"):
            self.destroy()


class LoginWindow(BaseWindow):
    def __init__(self, q: Queue):
        super().__init__(
            win_title = "用戶登入 / 註冊",
            height = 300
        )

        self.resizable(False, False)
        self.centerToScreen()
        
        # ==============================================================

        """ 輸入框顯示訊息 """

        PLACEHOLDER_EMAIL = "輸入電子信箱"
        PLACEHOLDER_PASSWORD = "輸入密碼"

        # ==============================================================

        """ 所有元件設置 """

        lbl_title = tk.Label(self, font=FONT_TEXT, text="登入帳號")
        self.entry_email = tk.Entry(self, font=FONT_ENTRY)
        self.entry_password = tk.Entry(self, font=FONT_ENTRY, name="entry-pwd")
        self.submit_btn = tk.Button(self, font=FONT_BTN, text="登入", command=lambda: self.login_user(q))
        self.register_btn = tk.Button(self, font=FONT_BTN, text="註冊", command=self.register_user)
        self.forgot_pwd_btn = tk.Button(self, font=FONT_BTN, text="忘記密碼", command=self.forgot_password)


        lbl_title.place(
            x = 170,    y =  10
        )
        self.entry_email.place(
            x = 100,    y =  80
        )
        self.entry_password.place(
            x = 100,    y = 150
        )
        self.submit_btn.place(
            x = 100,    y = 230
        )
        self.register_btn.place(
            x = 200,    y = 230
        )
        self.forgot_pwd_btn.place(
            x = 300,     y = 230
        )

        self.entry_email.insert(0, PLACEHOLDER_EMAIL)
        self.entry_email.configure(state='disabled')
        self.entry_password.insert(0, PLACEHOLDER_PASSWORD)
        self.entry_password.configure(state='disabled')

        # ---------------------------------------------------------

        # 滑鼠左鍵點擊: 消除顯示訊息
        self.entry_email.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_email))
        self.entry_password.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_password))
        
        # ---------------------------------------------------------
        
        # 離開目標輸入框: 重新顯示訊息
        self.entry_email.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_email, PLACEHOLDER_EMAIL))
        self.entry_password.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_password, PLACEHOLDER_PASSWORD))


    def register_user(self):
        win = SignUpWindow()
        win.grab_set()


    def login_user(self, q: Queue):
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        if self.entry_email.cget('state') != 'disabled' and not validate_email(email):
            messagebox.showerror("登入失敗 !", "Email 的格式錯誤 ! 請重新檢查格式是否正確")
            return
        
        fetch_result, _ = access_db.select(
            table_name="users",
            search_vals=[("email", email)],
            conditions=["="],
            fetch_columns=["email", "password"]
        )

        if not fetch_result:
            return

        hashed_pwd = fetch_result[0][1]
        print(hashed_pwd)

        if bcrypt.checkpw(password.encode(), hashed_pwd):
            q.put(email)
            messagebox.showinfo("登入", "登入成功 ! 進入遊戲 !")
            self.destroy()

        else:
            messagebox.showwarning("登入", "密碼錯誤 !")


    def forgot_password(self):
        win = ForgotPwdWindow()
        win.grab_set()


if __name__ == "__main__":
    table_create = """
                    CREATE TABLE IF NOT EXISTS `users` (
                            `id`          INTEGER         PRIMARY KEY     AUTOINCREMENT,
                            `email`       VARCHAR(100)    UNIQUE          NOT NULL,
                            `username`    VARCHAR(20)     NOT NULL,
                            `password`    VARCHAR(20)     NOT NULL,
                            `score`       INTEGER,
                            `max_lines`   INTEGER
                    );
                   """
    
    access_db.exec_cmd_sql(table_create)

    # win = MainWindow()
    queue = Queue()
    win = LoginWindow(queue)
    win.mainloop()

    if not queue.empty():
        tetris.main(queue.get())


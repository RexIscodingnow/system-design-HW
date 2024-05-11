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
from tkinter import messagebox
from base_window import BaseWindow, all_widgets_map


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

        lbl_title = tk.Label(self, font=FONT_TEXT, text="登入/註冊帳號")
        self.entry_email = tk.Entry(self, font=FONT_ENTRY)
        self.entry_username = tk.Entry(self, font=FONT_ENTRY)
        self.entry_password = tk.Entry(self, font=FONT_ENTRY, name="entry-pwd")
        self.register_btn = tk.Button(self, font=FONT_BTN, text="註冊", command=self.register_user)


        lbl_title.place(
            x = self.winfo_width() + 160,    y =  10
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

        # TODO: bcrypt
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

        messagebox.showinfo("註冊", "註冊成功 ! 請關閉註冊視窗 !")


class LoginWindow(BaseWindow):
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
        PLACEHOLDER_PASSWORD = "輸入密碼"

        # ==============================================================

        """ 所有元件設置 """

        lbl_title = tk.Label(self, font=FONT_TEXT, text="登入/註冊帳號")
        self.entry_email = tk.Entry(self, font=FONT_ENTRY)
        self.entry_password = tk.Entry(self, font=FONT_ENTRY, name="entry-pwd")
        self.submit_btn = tk.Button(self, font=FONT_BTN, text="登入", command=self.login_user)
        self.register_btn = tk.Button(self, font=FONT_BTN, text="註冊", command=self.register_user)


        lbl_title.place(
            x = 160,    y =  10
        )
        self.entry_email.place(
            x = 100,    y =  80
        )
        self.entry_password.place(
            x = 100,    y = 150
        )
        self.submit_btn.place(
            x = 160,    y = 230
        )
        self.register_btn.place(
            x = 260,    y = 230
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
        win.mainloop()
        

    def login_user(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        if self.entry_email.cget('state') != 'disabled' and not validate_email(email):
            messagebox.showerror("註冊失敗 !", "Email 的格式錯誤 ! 請重新檢查格式是否正確")
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
            messagebox.showinfo("登入", "登入成功 ! 進入遊戲 !")
            self.destroy()

        else:
            messagebox.showwarning("登入", "密碼錯誤 !")


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__(
            win_title="Main window",
            width=600,
            height=800
        )
        
        self.centerToScreen()
        # self.after(1000, self.open_login_window)
        # self.after(1200, self.open_info_window)

        # 創建一個 Frame 來放置 pygame 畫面
        embed = tk.Frame(self, width=500, height=500)
        embed.pack()
        

    # def closing_wins(self):
        # try:
        #     info_win.destroy()

        # except Exception as e:
        #     print(e)
    
        # finally:
        #     login_window.destroy()


    # def open_login_window(self):
    #     global login_window

    #     login_window = LoginWindow()

    #     try:
    #         login_window.protocol("WM_DELETE_WINDOW", self.closing_wins)
    
    #     except Exception as e:
    #         print(e)
        
    #     finally:
    #         login_window.mainloop()


    # def open_info_window(self):
    #     global info_win

    #     info_win = InfoWindow()
    #     info_win.mainloop()




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
    win = LoginWindow()
    win.mainloop()
    
    # tetris.main()

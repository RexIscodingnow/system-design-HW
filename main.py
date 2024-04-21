import os
import time
import pathlib
from base_window import BaseWindow, all_widgets_map

import tkinter as tk
from tkinter import messagebox
from config import *


class SignUp_Win(BaseWindow, tk.Toplevel):
    def __init__(self):
        super().__init__(
            win_title = "註冊使用者",
            height = 300
        )

        self.resizable(False, False)
        self.centerToScreen()


class LoginWindow(BaseWindow, tk.Toplevel):
    def __init__(self):
        super().__init__(
            win_title = "註冊使用者",
            height = 300
        )

        self.resizable(False, False)
        self.centerToScreen()
        
        # ==============================================================

        # 輸入框顯示訊息
        PLACEHOLDER_EMAIL = "輸入電子信箱"
        PLACEHOLDER_USERNAME = "輸入使用者名稱"
        PLACEHOLDER_PASSWORD = "輸入密碼"

        # ==============================================================

        # 所有元件設置
        lbl_title = tk.Label(self, font=FONT_TEXT, text="登入帳號")
        self.entry_email = tk.Entry(self, font=FONT_ENTRY)
        self.entry_username = tk.Entry(self, font=FONT_ENTRY)
        self.entry_password = tk.Entry(self, font=FONT_ENTRY, name="entry-pwd")
        self.submit = tk.Button(self, font=FONT_BTN, text="登入")


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
        self.submit.place(
            x = self.winfo_width() + 210,    y = 230
        )

        self.entry_email.insert(0, PLACEHOLDER_EMAIL)
        self.entry_email.configure(state='disabled')
        self.entry_username.insert(0, PLACEHOLDER_USERNAME)
        self.entry_username.configure(state='disabled')
        self.entry_password.insert(0, PLACEHOLDER_PASSWORD)
        self.entry_password.configure(state='disabled')


        # ==============================================

        self.entry_email.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_email))
        self.entry_username.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_username))
        self.entry_password.bind('<Button-1>', lambda event: self.focus_in_entry(self.entry_password))
        
        # ---------------------------------------------------------
        
        self.entry_email.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_email, PLACEHOLDER_EMAIL))
        self.entry_username.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_username, PLACEHOLDER_USERNAME))
        self.entry_password.bind('<FocusOut>', lambda event: self.focus_out_entry(self.entry_password, PLACEHOLDER_PASSWORD))

        # self.widgets_mapping = all_widgets_map(self)
        # print(self.widgets_mapping)

    


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__(
            win_title="Main window",
            height=700
        )
        
        self.centerToScreen()
        self.after(1000, self.open_login_window)


    def open_login_window(self):
        login_window = LoginWindow()
        login_window.grab_set()



if __name__ == "__main__":
    # win = MainWindow()
    win = LoginWindow()

    win.mainloop()


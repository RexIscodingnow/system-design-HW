import os
import time
import pathlib
from base_window import BaseWindow

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
        self.PLACEHOLDER_EMAIL = "輸入電子信箱 :"
        self.PLACEHOLDER_USERNAME = "輸入使用者名稱 :"
        self.PLACEHOLDER_PASSWORD = "輸入密碼 :"


        # ==============================================
        # ==============================================

        lbl_title = tk.Label(self, font=FONT_TEXT, text="登入帳號")
        self.entry_email = tk.Entry(self, font=FONT_ENTRY)
        self.entry_username = tk.Entry(self, font=FONT_ENTRY)
        self.entry_password = tk.Entry(self, font=FONT_ENTRY)
        self.submit = tk.Button(self, font=FONT_BTN, text="登入")

        self.entry_email.insert(0, self.PLACEHOLDER_EMAIL)
        self.entry_username.insert(0, self.PLACEHOLDER_USERNAME)
        self.entry_password.insert(0, self.PLACEHOLDER_PASSWORD)

        lbl_title.place(
            x=self.winfo_width() + 190, y=10
        )
        self.entry_email.place(
            x=self.winfo_width() + 100, y=80
        )
        self.entry_username.place(
            x=self.winfo_width() + 100, y=130
        )
        self.entry_password.place(
            x=self.winfo_width() + 100, y=180
        )
        self.submit.place(
            x=self.winfo_width() + 210, y=230
        )

        self.grid_columnconfigure(0, weight=1)

        # ==============================================

        self.bind('<FocusIn>', lambda event: self.focus_in())
        self.bind('<FocusOut>', lambda event: self.focus_out())

    
    def focus_out(self):
        if not self.entry_email.get():
            self.entry_email.insert(0, self.PLACEHOLDER_EMAIL)

        if not self.entry_username.get():
            self.entry_username.insert(0, self.PLACEHOLDER_USERNAME)

        if not self.entry_password.get():
            self.entry_password.insert(0, self.PLACEHOLDER_PASSWORD)


    def focus_in(self):
        if self.entry_email.get() == self.PLACEHOLDER_EMAIL:
            self.entry_email.delete(0, "end")

        if self.entry_username.get() == self.PLACEHOLDER_USERNAME:
            self.entry_username.delete(0, "end")

        if self.entry_password.get() == self.PLACEHOLDER_PASSWORD:
            self.entry_password.delete(0, "end")


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


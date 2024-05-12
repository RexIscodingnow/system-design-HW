import tkinter as tk
from tkinter import messagebox

import pathlib
from PIL import Image, ImageTk
from collections import namedtuple



class BaseWindow(tk.Tk):
    def __init__(self,
                 win_title: str | None = None,
                 width: int = 500,
                 height: int = 600,
                 *,
                 min_width: int = 0,
                 min_height: int = 0,
                 minSize: tuple[int] | None = None
                 ) -> None:
        """
        This is a template for any tkinter window to inherit.

        Parameters:

            - win_title: Set the title of the window

            - width: The width of the window size

            - height: The height of the window size

            - min_width: The minimum width of window size

            - min_height: The minimum height of window size

            - minSize: The first element represents width, and the second represents the height.
                       It sets both similar to `min_width` and `min_height`.
            
            >>> (500, 600)  <=>  min_width = 500, min_height = 600
            
        Properties:

            - image_path: Given an image path for background.   .
                          It can use relative path, absolute path to read it.
            
            >>> image_path = 'C:/Users/usr/images/abc.jpg'
            >>> image_path = './images/abc.jpg'
        """
        
        super().__init__()

        self.config(
            bg="black"
        )
        self.width = width
        self.height = height
        self.wm_title(win_title)
        self.old_size = namedtuple("old_size", ("width", "height"))
        self.old_size.width = self.winfo_width()
        self.old_size.height = self.winfo_height()
        
        # ===========================================================
        # ===========================================================

        """ set window size """
        
        self.geometry(f"{self.width}x{self.height}")
        
        if minSize is None:
            self.minsize(min_width, min_height)
        else:
            self.minsize(*minSize)
        

        # ===========================================================
        # ===========================================================

        """ background image """
        
        self.__img_path = ""
        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
    

    @property
    def image_path(self):
        return self.__img_path
    
    @image_path.setter
    def image_path(self, new_img_path: str):
        try:
            # self.__img_path = os.path.join(os.getcwd(), new_img_path)
            self.__img_path = pathlib.Path(new_img_path)
            # print(self.__img_path)
            self.bg_img = ImageTk.PhotoImage(Image.open(self.__img_path))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_img)
            self.canvas.place(x=0, y=0)
        
        except:
            messagebox.showerror(
                "Error Message",
                "提示：圖片載入出錯，請檢查該檔案是否存在該路徑"
            )

    
    def centerToScreen(self) -> None:
        """
        Position the window at the center screen coordinates.
        """
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = (screen_width - self.width) // 2
        center_y = (screen_height - self.height) // 2

        self.geometry(f"{self.width}x{self.height}+{center_x}+{center_y}")


    def focus_in_entry(self, entry: tk.Entry):
        """
        The entry is cleared when the focus is on it (the user is typing something)

        Parameters:

            - entry: an input textbox
        """
        
        if entry.cget('state') == 'disabled':
            entry.configure(state='normal')
            entry.delete(0, 'end')

            if entry.winfo_name() == "entry-pwd":
                entry.config(show="*")


    def focus_out_entry(self, entry: tk.Entry, placeholder: str):
        """
        The entry shows a placeholder message when the user is not typing.

        Parameters:

            - entry: an input textbox
            
            - placeholder: placeholder message
        """
        
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(state='disabled')

            if entry.winfo_name() == "entry-pwd":
                entry.config(show="")




def all_widgets_map(window: tk.Tk) -> dict[str, tk.Widget]:
    """
    Return a dictionary of all widget names and objects in the specified window
    
    Parameter
        - window: target window of Tk

    rtype: dictionary
            - key: Name of target widget
            - value: Widget
    """
    all_widgets = {}

    for widget in window.winfo_children():
        widget_name = widget.winfo_name()
        all_widgets[widget_name] = widget

    return all_widgets



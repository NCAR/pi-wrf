# importing standard modules 
import subprocess
import sys
import tkinter as tk
from PIL import Image, ImageTk

# importing local modules
from color_schemes      import color_scheme

# set color scheme and font
gui_color=color_scheme(1)                                            # 1=default

class SplashPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])

        frame = tk.Frame(self, relief='raised', borderwidth=2)
        frame.pack(fill="both", expand=True)
        frame.pack_propagate(False)


        self.image = Image.open("/pi-wrf/WRF_System/lib/logo_splash_image.jpg")
        self.img_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(frame, image=self.background_image)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.background.bind('<Configure>', self._resize_image)


        top_frame = tk.Frame(frame)
        top_frame.place(relx=0.5,rely=0.8,anchor='center')

        # continue button
        from Pages.start_page   import StartPage
        continue_btn = tk.Button(top_frame,
                          text='Continue',
                          font=('Arial Bold',40),
                          borderwidth=5,bg='white',
                          activebackground=gui_color[2],
                          width=10,
                          command=lambda : controller.show_frame(StartPage))
        continue_btn.pack()


    def _resize_image(self,event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

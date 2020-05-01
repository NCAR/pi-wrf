#Lily's Python TKinter/Pillow practice 1
#Displays colored rectangles

#Import libraries
import tkinter as tk
from PIL import Image, ImageTk

#set up master window and frame
master = tk.Tk()
frame = tk.Frame(master)
frame.pack(fill=tk.BOTH,expand=True)

#set up image
img_load = Image.open("test1.jpeg")
img_render = ImageTk.PhotoImage(img_load)

#set up label
label = tk.Label(frame,bg="blue")
label.pack(fill=tk.BOTH,expand=True)

#load image
label.config(image=img_render)

#start graphics
tk.mainloop()

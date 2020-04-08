#Lily's Python TKinter practice 1
#Displays colored rectangles

#Import libraries
import Tkinter as tk

#set up master window and frame
master = tk.Tk()
frame = tk.Frame(master)
frame.pack(fill=tk.BOTH,expand=True)

#set up subframes
sframe1 = tk.Frame(frame,bg="red")
sframe2 = tk.Frame(frame,bg="blue")
sframe1.pack(fill=tk.BOTH,expand=True)
sframe2.pack(fill=tk.BOTH,expand=True)

#start graphics
tk.mainloop()

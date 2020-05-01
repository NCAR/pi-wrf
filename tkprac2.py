#Lily's Python TKinter practice 2
#Displays colored rectangles side-by-side

#Import libraries
import Tkinter as tk

#set up master window and frame
master = tk.Tk()
frame = tk.Frame(master)
frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

#set up subframes
sframe1 = tk.Frame(frame,bg="blue")
sframe2 = tk.Frame(frame,bg="red")
sframe1.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
sframe2.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

#start graphics
tk.mainloop()

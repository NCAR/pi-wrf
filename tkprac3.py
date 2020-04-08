#Lily's Python TKinter practice 1
#Displays colored rectangles

#Import libraries
import Tkinter as tk

#set up master window and frame
master = tk.Tk()
frame = tk.Frame(master)
frame.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

#set up subframes
sframe1 = tk.Frame(frame)
sframe2 = tk.Frame(frame)
sframe1.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
sframe2.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

#set up sub-subframes for subframe 1
ssframe1 = tk.Frame(sframe1,bg="green")
ssframe2 = tk.Frame(sframe1,bg="red")
ssframe1.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
ssframe2.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

#set up sub-subframes for subframe 2
ssframe3 = tk.Frame(sframe2,bg="blue",width=20,height=200)
ssframe4 = tk.Frame(sframe2,bg="yellow",width=30,height=200)
ssframe5 = tk.Frame(sframe2,bg="pink",width=40,height=200)
ssframe3.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
ssframe4.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
ssframe5.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)


#start graphics
tk.mainloop()

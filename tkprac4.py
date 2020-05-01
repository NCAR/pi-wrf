#Lily's Python TKinter practice 4
#Displays multiple colored rectangles
#Uses place manager and subframes

#Import libraries
import Tkinter as tk

#set up master window and frame
master = tk.Tk()
frame = tk.Frame(master,bg="blue")
frame.pack(fill=tk.BOTH,expand=True)

#set up subframes
sframe1 = tk.Frame(frame,bg="pink",width=30,height=10)
sframe2 = tk.Frame(frame,bg="black",width=150,height=25)
sframe1.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
sframe2.place(relx=0,rely=0.85,anchor=tk.W)
sframe3 = tk.Frame(frame,bg="red",width=60,height=200)
sframe3.place(relx=0.15,rely=0.15,anchor=tk.CENTER)
sframe4 = tk.Frame(frame,width=60,height=200)
sframe4.place(relx=0.65,rely=0.15,anchor=tk.CENTER)

#set up sub-subframes
ssframe1 = tk.Frame(sframe4,bg="yellow",width=60,height=100)
ssframe1.pack(side=tk.TOP,expand=True,fill=tk.BOTH)
ssframe2 = tk.Frame(sframe4,bg="green",width=60,height=100)
ssframe2.pack(side=tk.TOP,expand=True,fill=tk.BOTH)


#start graphics
tk.mainloop()

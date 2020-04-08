#Lily's Python TKinter practice 1
#Displays colored rectangles

#Import libraries
import Tkinter as tk

#set up master window and frame
master = tk.Tk()
frame = tk.Frame(master,bg="blue")
frame.pack(fill=tk.BOTH,expand=True)

#set up subframes
sframe1 = tk.Frame(frame)
sframe2 = tk.Frame(frame)
sframe1.grid(row=0,column=0)
sframe2.grid(row=0,column=1)

#set up widgets
strlist = tk.StringVar()
strlist.set(('a','b','c','d'))
listbox = tk.Listbox(sframe1,listvariable=strlist)
listbox.pack()
label = tk.Label(sframe2,text="Testing 123")
label.pack()
button=tk.Button(sframe2,text="Label Set",
  command=lambda : (label.config(text=listbox.get(listbox.curselection()))))
button.pack()

#start graphics
tk.mainloop()

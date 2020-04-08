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

#set up sub-subframes
ssframe1 = tk.Frame(sframe2)
ssframe2 = tk.Frame(sframe2)
ssframe1.grid(row=0,column=0)
ssframe2.grid(row=1,column=0)

#set up widgets
strlist = tk.StringVar()
strlist.set(('a','b','c','d'))
listbox = tk.Listbox(sframe1,listvariable=strlist,selectmode=tk.SINGLE)
listbox.pack()
text = tk.Text(ssframe1)
text.pack(side=tk.LEFT)
scroll = tk.Scrollbar(ssframe1)
scroll.pack(side=tk.RIGHT,fill=tk.Y)
text.config(yscrollcommand=scroll.set)
scroll.config(command=text.yview)
button=tk.Button(ssframe2,text="Label Set",
  command=lambda : (text.insert(tk.END,listbox.get(listbox.curselection()) * 50)))
button.pack()

#start graphics
tk.mainloop()

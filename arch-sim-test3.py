#Lily's Python TKinter practice 1
#Displays colored rectangles

#Import libraries
import Tkinter as tk

#set up master window and frame
master = tk.Tk()
frame = tk.Frame(master,bg="gray")
frame.pack(fill=tk.BOTH,expand=True)

#set up subframes
sframe1 = tk.Frame(frame,bg="darkgray")
sframe2 = tk.Frame(frame)
sframe1.grid(row=0,column=0)
sframe2.grid(row=1,column=0)

#set up sub-subframes
ssframe1 = tk.Frame(sframe2)
ssframe2 = tk.Frame(sframe2)
ssframe1.grid(row=0,column=0)
ssframe2.grid(row=0,column=1)

#set up sub-sub-subframes
sssframe1 = tk.Frame(ssframe1)
sssframe2 = tk.Frame(ssframe1)
sssframe1.grid(row=0,column=0)
sssframe2.grid(row=1,column=0)

#set up widgets
#work on listbox layout next time
#work on textfield layout as well
strlist = tk.StringVar()
strlist.set(('a','b','c','d'))
listbox = tk.Listbox(sssframe1,listvariable=strlist,selectmode=tk.SINGLE)
listbox.pack()
label = tk.Label(sframe1,text="Testing")
label.pack()
text = tk.Text(ssframe2)
text.pack(side=tk.LEFT)
scroll = tk.Scrollbar(ssframe2)
scroll.pack(side=tk.RIGHT,fill=tk.Y)
text.config(yscrollcommand=scroll.set)
scroll.config(command=text.yview)
button=tk.Button(sssframe2,text="Label Set",
  command=lambda : (text.insert(tk.END,listbox.get(listbox.curselection()) * 50)))
button.pack()

#start graphics
tk.mainloop()

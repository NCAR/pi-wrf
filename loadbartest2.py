#Lily's Python loading bar example 2

#import libraries
import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen

#create functions
def prep_download(addr):

  response = urlopen(addr)
  file_size = int(response.headers['Content-Length'])

  def chunk_download(readdata=0):

    load_percent = readdata * 100 / file_size
    loadbar['value'] = load_percent

    current_data = response.read(10)
    if not current_data:
      return
    else:
      text.insert(current_data)
      master.after(0,chunk_download,readdata + len(current_data))

#create master window
master = tk.Tk()
frame = tk.Frame(master)
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
sssframe3 = tk.Frame(ssframe2)
sssframe1.grid(row=0,column=0)
sssframe2.grid(row=1,column=0)
sssframe3.grid(row=0,column=0)

#set up widgets
#strlist = tk.StringVar()
#strlist.set(('a','b','c','d'))
#listbox = tk.Listbox(sssframe1,listvariable=strlist,selectmode=tk.SINGLE)
#listbox.pack()
#listbox.select_set(0)
#listbox.event_generate("<<ListboxSelect>>")
loadbar = ttk.Progressbar(sssframe1,length=150)
loadbar.pack()
label = tk.Label(sframe1,text="Testing")
label.pack()
label2 = tk.Label(sssframe3,bg="blue")
label2.pack()
text = tk.Text(sssframe3)
text.pack(side=tk.LEFT)
#text.insert(tk.END,blahblah[0])
#text.delete("1.0",tk.END)
scroll = tk.Scrollbar(sssframe3)
scroll.pack(side=tk.RIGHT,fill=tk.Y)
text.config(yscrollcommand=scroll.set)
scroll.config(command=text.yview)
button=tk.Button(sssframe2,text="Confirm")
#command=lambda : run_swap(text,blahblah[listbox.curselection()[0]],label2,("tes$
button.pack()
button2=tk.Button(sssframe2,text="Back")
button2.pack()

#start graphics
tk.mainloop()

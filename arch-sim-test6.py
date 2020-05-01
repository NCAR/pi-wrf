#WRF-Pi Archived Simulations example script final version

#Import libraries
import tkinter as tk
from PIL import Image, ImageTk

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
sssframe3 = tk.Frame(ssframe2)
sssframe1.grid(row=0,column=0)
sssframe2.grid(row=1,column=0)
sssframe3.grid(row=0,column=0)

#set up button command functions
#text box contents swap function
def display_blahblah(textbox,newtext):

  textbox.delete("1.0",tk.END)
  textbox.insert(tk.END,newtext)

#label image swap function
def display_image(label,imgpath):

  newimg_load = Image.open(imgpath)
  newimg_render = ImageTk.PhotoImage(newimg_load)
  label.configure(image=newimg_render)
  label.image=newimg_render

#multirunning function
def run_swap(textbox,newtext,label,imgpath):

  display_blahblah(textbox,newtext)
  display_image(label,imgpath)

#load initial image
img_load = Image.open("test1-1.gif")
img_render = ImageTk.PhotoImage(img_load)

#set up textfile strings
blahblah = ["blahblah1","blahblah2","blahblah3","blahblah4"]
for num in range(0,4):

  file = open("read" + str(num + 1) + ".txt","r")
  blahblah[num] = file.read()
  file.close()

#set up widgets
strlist = tk.StringVar()
strlist.set(('a','b','c','d'))
listbox = tk.Listbox(sssframe1,listvariable=strlist,selectmode=tk.SINGLE)
listbox.pack()
listbox.select_set(0)
listbox.event_generate("<<ListboxSelect>>")
label = tk.Label(sframe1,text="Testing")
label.pack()
label2 = tk.Label(sssframe3,bg="blue")
label2.pack()
text = tk.Text(sssframe3)
text.pack(side=tk.LEFT)
text.insert(tk.END,blahblah[0])
text.delete("1.0",tk.END)
scroll = tk.Scrollbar(sssframe3)
scroll.pack(side=tk.RIGHT,fill=tk.Y)
text.config(yscrollcommand=scroll.set)
scroll.config(command=text.yview)
#print(listbox.curselection())
#print(listbox.curselection()[0])
button=tk.Button(sssframe2,text="Confirm",
command=lambda : run_swap(text,blahblah[listbox.curselection()[0]],label2,("test1-" + str((listbox.curselection()[0] + 1)) + ".gif")))
button.pack()
button2=tk.Button(sssframe2,text="Back")
button2.pack()

#display initial image
label2.configure(image=img_render)
label2.image=img_render

#start graphics
tk.mainloop()



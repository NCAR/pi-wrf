# importing standard library modules
import sys
import tkinter as tk

# importing local modules
from color_schemes      import color_scheme
from Pages.splash_page  import SplashPage
from Pages.start_page   import StartPage
from Pages.page_one     import PageOne
from Pages.page_two     import PageTwo
from Pages.page_three   import PageThree
from Pages.page_four    import FigurePage

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('WRF Sim')                                        #set the title of the main window
        screenwidth=self.winfo_screenwidth()                         #get the current screen width
        screenheight=self.winfo_screenheight()                       #current height of screen
        self.geometry('%dx%d'%(screenwidth,screenheight))            #makes the main window fullscreen

 
        # this container stores all the pages
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)         #use pack geometry manger to layout container
        container.grid_rowconfigure(0, weight=1)                     #preemptively configuring rows for page widgets
        container.grid_columnconfigure(0,weight=1)                   #preemptively configuring columns for page widgets
        self.frames = {}                                             #dictionary of Pages to navigate To
        for F in (SplashPage,StartPage,PageOne,
                  PageTwo,PageThree,FigurePage):
            frame = F(container, self)                               #load pages
            self.frames[F] = frame                                   #store into frames
            frame.grid(row=0, column=0, sticky='nsew')               #place frames with grid. Settings inherited from container
        self.show_frame(SplashPage)                                  #make SplashPage show upfront
 
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def quit_app(self):
        app.destroy()
        sys.exit()

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()

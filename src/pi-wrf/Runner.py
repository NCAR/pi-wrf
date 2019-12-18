#Importing modules 
import sys
from importlist import *

#Set Color Scheme and Font
gui_color=color_scheme(1)                                            # 1=default
LARGE_FONT = ("Verdana", 12)

from Pages.start_page   import StartPage
from Pages.page_one     import PageOne
from Pages.page_two     import PageTwo
from Pages.page_three   import PageThree
from Pages.page_four    import FigurePage


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("WRF Sim")                                        # set the title of the main window
        global screenwidth, screenheight
        screenwidth=self.winfo_screenwidth()                         # get the current screen width
        screenheight=self.winfo_screenheight()                       # current height of screen
        self.geometry('%dx%d'%(screenwidth,screenheight))            # makes the main window fullscreen

 
        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)                     # make the cell in grid cover the entire window
        container.grid_columnconfigure(0,weight=1)                   # make the cell in grid cover the entire window
        self.frames = {}                                             # Dictionary of Pages to Navigate To
        for F in (StartPage,PageOne,PageTwo,PageThree,FigurePage):
            frame = F(container, self)                               # create the page
            self.frames[F] = frame                                   # store into frames
            frame.grid(row=0, column=0, sticky="nsew")               # grid it to container
 
        self.show_frame(StartPage)                                   # Make StartPage show upfront
 
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def quit_app(self):
        app.destroy()
        sys.exit()

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()

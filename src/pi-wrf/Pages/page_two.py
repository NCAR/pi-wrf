# importing standard modules
from matplotlib.backends.backend_tkagg   import FigureCanvasTkAgg
from matplotlib.widgets   import RectangleSelector
import matplotlib
import matplotlib.pyplot as plt
import pickle
from statistics   import mean
import tkinter as tk
from tkinter import messagebox

# importing local modules
from calculate_distance import calculate_distance
from color_schemes      import color_scheme
from set_domain         import set_domain

# importing 3rd party modules
from mpl_toolkits.basemap  import Basemap
import numpy as np

#Set Color Scheme and Font
gui_color=color_scheme(1)                                            # 1=default

global default_lat_limits,default_lon_limits
default_lat_limits   = [-90,90]
default_lon_limits   = [-180,180]

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])    
        gridcells = 566667

        
        def line_select_callback(eclick, erelease):
            """ Extracting corners of user defined rectangle
                This works by ingesting mouseclick data as arguments
                and calculating the spatial area and amount of grid cells.
                Based on the gridcell count it will either generate an error
                prompt or crop the map into a new domain """
            
            global xlim, ylim, gridcells
            temp_xlim=np.sort(np.array([erelease.xdata,eclick.xdata]))
            temp_ylim=np.sort(np.array([erelease.ydata,eclick.ydata]))
            domain_x_length=calculate_distance(min(temp_xlim),
                                                   max(temp_xlim),
                                                   mean([min(temp_ylim),max(temp_ylim)]),
                                                   mean([min(temp_ylim),max(temp_ylim)]))
            domain_y_length=calculate_distance(min(temp_xlim),
                                                   min(temp_xlim),
                                                   min(temp_ylim),
                                                   max(temp_ylim))
            domain_area=domain_x_length*domain_y_length
            gridcells=round(domain_area/30/30)
                        
            if gridcells < 100:
                messagebox.showwarning(title="Domain too small",
                                          message="At least 100 gridcells are needed. "
                                                  "Please click   and drag a larger "
                                                  "domain or click zoom out.")
            else:
                xlim = temp_xlim
                ylim = temp_ylim
                gridcells_lbl.configure(text="Approximate # of gridcells : {:,}".format(gridcells))
                ax.set_xlim(xlim)
                ax.set_ylim(ylim) 
                canvas.show()
                toggle_selector.RS.update()
        

        def toggle_selector(event):
            """ used to allow rectangle to persist and interact with if necessary"""
            print(' Key pressed.')
            if event.key in ['Q', 'q'] and toggle_selector.RS.active:
                toggle_selector.RS.set_active(False)
            if event.key in ['A', 'a'] and not toggle_selector.RS.active:
                toggle_selector.RS.set_active(True)
        
        def reset_domain(lons,lats):
            """ Resets the map and domain to the entire globe"""
               
            global gridcells, xlim, ylim
            ax.set_xlim(lons)
            ax.set_ylim(lats)
            gridcells=round(510000000/(30*30))
            gridcells_lbl.configure(text="Approximate # of gridcells : {:,}".format(gridcells))
            
            # Overriding the drawn rectangle to a zero value so it clears previous mouse clicks
            temp_list = [0,0,0,0]
            toggle_selector.RS.extents = tuple(temp_list)
            canvas.show()

            # Overriding steps create new rectangle and this clears the drawn rectangle
            for artist in toggle_selector.RS.artists:
                artist.set_visible(False)
            toggle_selector.RS.update() 

        def zoom_out():
            """ Forces the map to pan out """
            
            global xlim, ylim, gridcells
            length_x=abs(xlim[1]-xlim[0])
            length_y=abs(ylim[1]-ylim[0])
            
            # Handeling map edges
            if length_x < 10:
                zoom_out_x_lim=[xlim[0]-10,xlim[1]+10]
                if zoom_out_x_lim[0] < -180:
                    zoom_out_x_lim[0]=-180
                if zoom_out_x_lim[1] > 180:
                    zoom_out_x_lim[1]= 180
                ax.set_xlim(zoom_out_x_lim)
                
            if length_x >= 10:
                zoom_out_x_lim=[xlim[0]-length_x,xlim[1]+length_x]
                if zoom_out_x_lim[0] < -180:
                    zoom_out_x_lim[0]=-180
                if zoom_out_x_lim[1] > 180:
                    zoom_out_x_lim[1]= 180
                ax.set_xlim(zoom_out_x_lim)

            if length_y < 10:
                zoom_out_y_lim=[ylim[0]-10,ylim[1]+10]
                if zoom_out_y_lim[0] < -90:
                    zoom_out_y_lim[0]=-90
                if zoom_out_y_lim[1] > 90:
                    zoom_out_y_lim[1]= 90
                ax.set_ylim(zoom_out_y_lim)

            if length_y > 10:
                zoom_out_y_lim=[ylim[0]-length_y,ylim[1]+length_y]
                if zoom_out_y_lim[0] < -90:
                    zoom_out_y_lim[0]=-90
                if zoom_out_y_lim[1] > 90:
                    zoom_out_y_lim[1]= 90
                ax.set_ylim(zoom_out_y_lim)
                
            xlim=zoom_out_x_lim
            ylim=zoom_out_y_lim
            
            # Overriding the drawn rectangle to a zero value so it clears previous mouse clicks
            temp_list = list(toggle_selector.RS.extents)
            temp_list[0] = xlim[0]
            temp_list[1] = xlim[1]
            temp_list[2] = ylim[0]
            temp_list[3] = ylim[1]
            temp_list = [0,0,0,0]
            toggle_selector.RS.extents = tuple(temp_list)
            toggle_selector.RS.update()
            canvas.show()

            # Overriding steps create new rectangle and this clears the drawn rectangle
            for artist in toggle_selector.RS.artists:
                artist.set_visible(False)
            toggle_selector.RS.update()

            
            # Calculating the spatial area and amount of grid cells.
            domain_x_length=calculate_distance(min(xlim),
                                                     max(xlim),
                                                     mean([min(ylim),max(ylim)]),
                                                     mean([min(ylim),max(ylim)]))
            domain_y_length=calculate_distance(min(xlim),
                                                     min(xlim),
                                                     min(ylim),
                                                     max(ylim))
            domain_area=domain_x_length*domain_y_length
            gridcells=round(domain_area/30/30)
            gridcells_lbl.configure(text="Approximate # of gridcells : {:,}".format(gridcells))
        
        def domain_maxsize_check():
            """ Checks the number of gridcells. If too many gridcells it generates error prompt """
            
            global gridcells
            try: gridcells
            except NameError: gridcells = 566667
            if gridcells > 15000:
                tk.messagebox.showwarning(title="Domain too large",
                                          message= "The domain is too large to run a simulation. "
                                                   "Please select a domain less than 15,000 grid cells.")
            else:
                set_domain(xlim,ylim)
                controller.show_frame(PageThree)
                reset_domain(default_lon_limits,default_lat_limits)

                
        ## Creating page and frames ##
        frame1_topbanner=tk.Frame(self)
        frame1_topbanner.pack(side=tk.TOP,fill=tk.X)
        topbanner_lbl = tk.Label(frame1_topbanner,
                                 text="Choose Domain and Resolution",
                                 font=('Arial Bold',40),
                                 bg=gui_color[1])
        topbanner_lbl.pack(fill=tk.X)
        
        frame2_toolbar=tk.Frame(self)
        frame2_toolbar.pack(fill=tk.X)
               
        frame2_map=tk.Frame(self)
        frame2_map.pack(fill=tk.X,side=tk.BOTTOM,expand=0)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor(gui_color[0])
    
        reset_btn=tk.Button(frame2_toolbar,
                            text="Reset Domain",
                            font=('Arial Bold',10),
                            command=lambda : reset_domain(default_lon_limits,default_lat_limits))
        reset_btn.pack(side=tk.LEFT)
        
        zoomout_btn=tk.Button(frame2_toolbar,
                              text="Zoom Out",
                              font=('Arial Bold',10),
                              command=lambda :  zoom_out())
        zoomout_btn.pack(side=tk.LEFT)
        
        gridcells=round(510000000/(30*30))
        gridcells_lbl=tk.Label(frame2_toolbar,
                               text='Approximate # of gridcells : {}'.format(gridcells),
                               font=('Arial Bold',10))
        gridcells_lbl.pack(side=tk.RIGHT)
        
        # Creating buttons on page
        from Pages.page_two   import PageTwo
        from Pages.start_page   import StartPage
        home_btn = tk.Button(frame2_map,
                             text="Home",
                             bg=gui_color[2],
                             activebackground=gui_color[3],
                             command=lambda :[reset_domain(default_lon_limits,default_lat_limits),
 					         controller.show_frame(StartPage)])
        home_btn.pack(side=tk.LEFT,fill=tk.X)

        from Pages.page_three import PageThree
        confirm_dom_btn = tk.Button(frame2_map,
                                    text="Confirm Domain",
                                    bg=gui_color[2],
                                    activebackground=gui_color[3],
                                    command=lambda : [domain_maxsize_check()])
        confirm_dom_btn.pack(side=tk.RIGHT,fill=tk.X)
        
        # Creating Matplotlib figure
        pkfile='map.pkl'
        m=pickle.load(open(pkfile,'rb'))
        fig, ax = plt.subplots(1,1)
        m.ax=ax
        
        # uncomment to override pickled map
        #m=Basemap(projection='cyl',
        #          llcrnrlat=-90,
        #          urcrnrlat=90,
        #          llcrnrlon=-180,
        #          urcrnrlon=180,
        #          resolution='c',
        #          area_thresh=1,
        #          ax=ax)
        
        m.drawcoastlines(color='white',linewidth=.5)
        m.fillcontinents(color='forestgreen',lake_color='cornflowerblue')
        lat_lines=m.drawparallels(np.arange(-90,91,30))
        lon_lines=m.drawmeridians(np.arange(-180,181,60))
        m.drawmapboundary(fill_color='cornflowerblue')
        m.drawcountries(color='white')
        m.drawstates(color='white')
        
        # uncomment to save map opbject
        #pickle.dump(m, open('map.pkl','wb'))
        
        canvas=FigureCanvasTkAgg(fig,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        canvas._tkcanvas.pack(side=tk.BOTTOM)
 
        # Creating rectangle selector and binding it (again, this should be removed)
        toggle_selector.RS = RectangleSelector(ax,
                                               line_select_callback, 
                                               drawtype='box', 
                                               useblit=True, 
                                               interactive=False,
                                               lineprops=dict(color='black',linewidth=4),
                                               rectprops=dict(facecolor='black',
                                                              edgecolor='black',
                                                              alpha=.4,
                                                              fill=True))
        plt.connect('key_press_event', toggle_selector) 
        

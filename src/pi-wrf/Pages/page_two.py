#Importing modules 
import sys
from importlist import *
import pickle
#Set Color Scheme and Font
gui_color=color_scheme(1)                                            # 1=default
LARGE_FONT = ("Verdana", 12)

global default_lat_limits,default_lon_limits
default_lat_limits   = [-90,90]
default_lon_limits   = [-180,180]


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])    


########################################################################################################################################################
########################################################################################################################################################
#### Functions for Interactive Non-Tiling Map
        
        # Extracting corners of user defined rectangle
        def line_select_callback(eclick, erelease):
            global xlim, ylim
            xlim=np.sort(np.array([erelease.xdata,eclick.xdata]))
            ylim=np.sort(np.array([erelease.ydata,eclick.ydata]))
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            domain_x_length=ds.calculate_distances(min(xlim),
                                                   max(xlim),
                                                   mean([min(ylim),max(ylim)]),
                                                   mean([min(ylim),max(ylim)]))
            domain_y_length=ds.calculate_distances(min(xlim),
                                                   min(xlim),
                                                   min(ylim),
                                                   max(ylim))
            domain_area=domain_x_length*domain_y_length
            gridcells=round(domain_area/30/30)
            lbl_gridcells.configure(text='Approximate # of gridcells : {:,}'.format(gridcells))
            canvas.show()

        # This should be removed becuase it isn't needed for this program.
        def toggle_selector(event):
            print(' Key pressed.')
            if event.key in ['Q', 'q'] and toggle_selector.RS.active:
                #print(' RectangleSelector deactivated.')
                toggle_selector.RS.set_active(False)
            if event.key in ['A', 'a'] and not toggle_selector.RS.active:
                #print(' RectangleSelector activated.')
                toggle_selector.RS.set_active(True)
        
        def reset_domain(lons,lats):
            ax.set_xlim(lons)
            ax.set_ylim(lats)
            gridcells=round(510000000/(30*30))
            lbl_gridcells.configure(text='Approximate # of gridcells : {:,}'.format(gridcells))
            canvas.show()
              
        def zoom_out():
            global xlim, ylim
            length_x=abs(xlim[1]-xlim[0])
            length_y=abs(ylim[1]-ylim[0])
            
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
                

            canvas.show()
            xlim=zoom_out_x_lim
            ylim=zoom_out_y_lim
            del length_x
            del length_y

#### End Functions for Interactive Non-Tiling Map 
########################################################################################################################################################
########################################################################################################################################################
                
        # Creating page and frames
        frame1_topbanner=tk.Frame(self)
        frame1_topbanner.pack(side=tk.TOP,fill=tk.X)
        topbanner = tk.Label(frame1_topbanner,
                             text="Choose Domain and Resolution",
                             font=("Arial Bold",40),
                             bg=gui_color[1])
        topbanner.pack(fill=tk.X)
        
        frame2_toolbar=tk.Frame(self)
        frame2_toolbar.pack(fill=tk.X)
               
        frame2_map=tk.Frame(self)
        frame2_map.pack(fill=tk.X,side=tk.BOTTOM,expand=0)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor(gui_color[0])
    
        btn_reset=tk.Button(frame2_toolbar,
                            text="Reset Domain",
                            font=("Arial Bold",10),
                            command=lambda : reset_domain(default_lon_limits,default_lat_limits))
        btn_reset.pack(side=tk.LEFT)
        
        btn_zoom_out=tk.Button(frame2_toolbar,
                               text="Zoom Out",
                               font=("Arial Bold",10),
                               command=lambda :  zoom_out())
        btn_zoom_out.pack(side=tk.LEFT)
        
        gridcells=round(510000000/(30*30))
        lbl_gridcells=tk.Label(frame2_toolbar,
                               text="Approximate # of gridcells : {}".format(gridcells),
                               font=("Arial Bold",10))
        lbl_gridcells.pack(side=tk.RIGHT)
        
        # Creating buttons on page
        from Pages.page_two   import PageTwo
        from Pages.start_page   import StartPage
        btn_1 = tk.Button(frame2_map,
                          text="Home",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda :[reset_domain(default_lon_limits,default_lat_limits), 
 					   controller.show_frame(StartPage)])
        btn_1.pack(side=tk.LEFT,fill=tk.X)

        from Pages.page_three import PageThree
        btn_2 = tk.Button(frame2_map,
                          text="Confirm Domain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [ds.set_domain(xlim,ylim),controller.show_frame(PageThree),
                                            reset_domain(default_lon_limits,default_lat_limits)])
        btn_2.pack(side=tk.RIGHT,fill=tk.X)
        
        # Creating Matplotlib figure
        

        pkfile='map.pkl'
        m=pickle.load(open(pkfile,'rb'))
        fig, ax = plt.subplots(1,1)
        m.ax=ax
        #m=Basemap(projection='cyl',
        #          llcrnrlat=-90,
        #          urcrnrlat=90,
        #          llcrnrlon=-180,
        #          urcrnrlon=180,
        #          resolution='l',
        #          area_thresh=1,
        #          ax=ax)
        m.drawcoastlines(color="white",linewidth=.5)
        m.fillcontinents(color='forestgreen',lake_color='cornflowerblue')
        test_hline=m.drawparallels(np.arange(-90,91,30))
        test_vline=m.drawmeridians(np.arange(-180,181,60))
        m.drawmapboundary(fill_color='cornflowerblue')
        m.drawcountries(color="white")
        m.drawstates(color="white")
        
        canvas =FigureCanvasTkAgg(fig,self)
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
                                               rectprops=dict(facecolor="black",edgecolor='black',alpha=.4,fill=True))
        plt.connect('key_press_event', toggle_selector) 
        

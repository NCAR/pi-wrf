#Tkinter GUI Modules
from PIL import Image 
from PIL import ImageTk
import datetime as dt
import tkinter  as tk

#Math Modules
from statistics import mean
import numpy as np


#Plotting Modules
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure                 import Figure
from matplotlib.widgets                import RectangleSelector
from mpl_toolkits.basemap              import Basemap
import matplotlib
import matplotlib.image  as mpimg
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


#System Modules
from collections import OrderedDict
from textwrap    import dedent
import matplotlib.cbook
import os
import warnings
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


#Multithreading Modules
from itertools  import islice
from subprocess import Popen, PIPE
from threading  import Thread
from queue      import Queue, Empty
import subprocess

#from wrf_model_domain_settings import * as ds
from color_schemes     import color_scheme
import wrf_model_domain_settings as ds
import User_calendar as wrf_calendar








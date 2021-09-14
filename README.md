This repository hosts a Jupyter Notebook application of the Weather Research and Forecasting Model (WRF) on a Raspberry Pi (version 3 or higher). The following text can be summarized into a few instructions to install and run the application. :<br/>
1) Open a terminal
2) Type `curl -sSL https://get.docker.com | sh`
3) Type `sudo docker run ncar/pi-wrf`
note: these instructions runs the pi-wrf notebook in a non-persistant state (any changes to the notebook will not be saved). To run the notebook so changes are saved, you will need to clone NCAR's Pi-WRF repo: [Pi-WRF](https://github.com/NCAR/pi-wrf "Pi-WRF"). Then, instead of step #3 above, Type `docker run -p 8888:8888 -v ~/pi-wrf/envs/smpar_gui/notebooks:/pi-wrf/src/notebooks ncar/piwrf`. The path after -v will need to be modified depending on where you clone the Pi-WRF repo in your file system.



### Section 1: Installing and Running the App (Raspberry Pi)
The Pi-WRF application requires an internet connection, and the container platform [Docker](https://www.docker.com/products/docker-desktop "Docker.com") to run. In short, Docker is a is a platform that creates containers, which simulates the software of a different computer, all within your own computer. If you are familiar with the term virtual machine, then containers are light-weight forms of virtual machines. The containers Docker creates are self-contained, and code/programs within the container do no affect any of the files or security on your host system. 

In order to run the Pi-WRF application, you will need to download and install Docker. Once this is completed, you will then download a Docker image and create a container which houses the Pi-WRF application. After the container is created you will run the program. The following instructions will inform you of how to download and install docker, create a container, and run the app.

1) Open a terminal by clicking on the following icon in the upper left of your screen. If you do not see the icon, you may press the following keys:<br/>
`Control` + `Alt` + `t` 

2) Download and install Docker (this may take upwards of 10 minutes) by typing the following in the terminal. This step only needs to be done once. Subsequent use of the app will not require this step.:<br/>
`curl -sSL https://get.docker.com | sh`:<br/>

3) Download a Docker image and create a container that holds the WRF app by typing the following (all in one line):<br/>
`sudo docker run reidolson/piwrf_notebook`
note: these instructions runs the piwrf notebook in a non-persistant state (any changes to the notebook will not be saved). To run the notebook so changes are saved, you will need to clone NCAR's Pi-WRF repo: [Pi-WRF](https://github.com/NCAR/pi-wrf "Pi-WRF"). Then, instead of step #3 above, Type `docker run -p 8888:8888 -v ~/pi-wrf/envs/smpar_gui/notebooks:/pi-wrf/src/notebooks ncar/pi-wrf`. The path after -v will need to be modified depending on where you clone the Pi-WRF repo in your file system.


### Section 2: Using the App
After the Docker container starts, there will be a URL in the terminal the user can copy and paste into their browser. This will open a locally hosted instance of Jupyter Notebook. The user should select the Pi-WRF.ipynb notebook which will open in a new tab. The notebook provides instructions for selecting the domain and the datetime range for the model. In order to use the application, the raspberry Pi must be connected to the internet. :<br/>

 
### Section 3: Uninstalling Docker
If you no longer wish to have the app or Docker installed on your Raspberry Pi you can remove all components without affected your Pi. To uninstall Docker and remove all containers you must enter the following commands into your terminal.:<br/>
1) Remove all containers:<br/>
`sudo docker system prune -a`:<br/>
2) Remove all images:<br/>
`sudo docker rmi $(docker images -a -q)`:<br/>


3) Remove Docker:<br/>
`Sudo apt remove docker-ce`:<br/>

### Section 4: Build from Source (advanced users only)
This section is for users who have modified the WRF source code. Make your changes to the source code and then run the following commands to build a new Docker Image. Warning: This may take a few hours to complete.

1) CD into the top level directory

2) Build the image with the command :<br/>
`docker build -f envs/smpar_gui/dockerfile .`

### Section 5: Miscellaneous Commands and Troubleshooting
1) App is not exiting
To force the app to quit press the following keys: 
`Control` + `c` 

2) Not responsive at start
At startup, the app loads. You will need to wait a few seconds once you see the home screen buttons. Once they highlight when you hover your mouse cursor over them, you may begin to use the app. 

3) Cannot run global simulation
Due to memory constraints of the Raspberry Pi, the app cannot run global simulations. Choose a smaller domain to run the model (we suggest less than 2,000 grid cells for efficiency).

4) I receive a segmentation error when running a simulation near the equator
At the equator, large towering cumulus clouds that arise due to deep convection are prevalent throughout the year. These clouds are associated with very strong updrafts or quickly moving rising air. The air moves so fast within the model, that the air can skip a vertical grid cell. The model does not know how to handle blank grid cells, so it produces an error. This is resolved be reducing the time step so the air will not travel as far in a shorter amount of time. 

5) Dates do not work 
Users are limited to a few days before the current date. Times prior to this are considered archived simulations and a collection of archive simulations will be included at a later version of the Pi-WRF application. 



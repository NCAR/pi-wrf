# Use the official Ubuntu base image
FROM ubuntu:jammy

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ="America/New_York"

# Install necessary dependencies
RUN apt-get update --fix-missing
RUN apt-get autoclean && apt-get install -y build-essential
RUN apt-get install -y    wget   \
    csh                          \
    nco                          \
    m4                           \
    libpng-dev                   \
    gfortran                     \
    file                         \
    make                         \
    curl                         \
    g++                          \
    libpng16-16                  \
    libgfortran5                 \
    # libnetcdf15                  \
    # libproj15                    \
    # libgdal26                    \
    imagemagick                  \
    libhdf5-103                  \
    mpich                        \
    ncl-ncarg                    \
    unzip                        \
    libxml2-dev                  \
    libbsd-dev

# Set up Python 3.10 and python libraries
RUN apt-get install -y python3   \
    python3-pip                  \
    python3-dev                  \
    python3-pil.imagetk          \
    python3-matplotlib           \
    python3-mpltoolkits.basemap   && \
    apt-get clean -y              && \
    apt-get autoremove


# Create a symlink to make 'python' refer to 'python3'
RUN ln -s /usr/bin/python3 /usr/bin/python    && \
    pip install requests jupyter              && \
    pip install ipyleaflet tzwhere            && \
    pip install hvplot ffmpeg                 && \
    pip install scipy                         && \
    pip install geocat-comp                   && \
    pip install netCDF4                       && \
    pip install cfgrib                        && \
    pip install -U matplotlib                 && \
    pip install -U matplotlib                 && \
    pip install xarray "xarray[viz]"          && \
    pip uninstall PIL                         && \
    pip install Pillow                        && \
    pip install folium

# Setting environment variable
ENV DIR=/pi-wrf/WRF_System/lib/LIBRARIES                       \
    WRF_DIR=/pi-wrf/WRF_System/WRFV4.5
ENV CC=gcc                                                     \
    CXX=g++                                                    \
    FC=gfortran                                                \
    F77=gfortran                                               \
    FFLAGS=-m64                                                \
    LDFLAGS=-L${DIR}/grib2/lib                                 \
    CPPFLAGS=-I${DIR}/grib2/include                            \
    JASPERLIB=${DIR}/grib2/lib                                 \
    JASPERINC=${DIR}/grib2/include                             \
    NETCDF=${DIR}/netcdf                                       \
    WRFIO_NCD_LARGE_FILE_SUPPORT=1
# Whole Path
ENV PATH=${DIR}/netcdf/bin:${PATH}
ENV PATH=${DIR}/mpich/bin:${PATH}
ENV PATH=${DIR}/grib2/bin:${PATH}
ENV PATH=${DIR}/hdf5/bin:${PATH}
ENV PATH=${DIR}/bin:${PATH}
# NETCDF Zlib Linking ENVs
ENV LIBS="-lnetcdf -lz"

ENV NETCDF_classic=1

# Setting up directories
RUN mkdir -p /pi-wrf/WRF_System/lib/LIBRARIES         && \
    mkdir /pi-wrf/WRF_System/lib/DATA/                && \
    mkdir -p /pi-wrf/pi_wrf/pi_wrf                    && \
    mkdir -p /pi-wrf/pi_wrf/pi_wrf/Pages              && \
    mkdir -p /pi-wrf/Output/user_saved_files          && \
    mkdir -p /pi-wrf/WRF_System/Plotting_Scripts

# DOWNLOADING WRF 4.5.2
RUN cd /pi-wrf/WRF_System/                                                  && \
    curl -O -L -J -k https://github.com/wrf-model/WRF/releases/download/v4.5.2/v4.5.2.tar.gz      && \
    tar -zxvf /pi-wrf/WRF_System/v4.5.2.tar.gz -C /pi-wrf/WRF_System/    && \
    rm /pi-wrf/WRF_System/*.gz

# DOWNLOADING WPS 4.5
RUN cd /pi-wrf/WRF_System/                                                         && \
    curl -O -L -J -k https://github.com/wrf-model/WPS/archive/refs/tags/v4.5.tar.gz      && \
    tar -zxvf /pi-wrf/WRF_System/WPS-4.5.tar.gz -C /pi-wrf/WRF_System/             && \
    mv WPS-4.5 WPS                                                                 && \
    rm *.gz

# DOWNLOADING STATIC DATA for WPS 4.5
RUN cd /pi-wrf/WRF_System/lib/                                                                               \
    && wget --no-check-certificate http://www2.mmm.ucar.edu/wrf/src/wps_files/geog_low_res_mandatory.tar.gz     \
    && tar xvf geog_low_res_mandatory.tar.gz                                                                    \
    && mv WPS_GEOG_LOW_RES WPS_GEOG                                                                             \
    && rm *.gz

#  INSTALLING MPICH LIBRARY
RUN cd $DIR/												           \
    && curl -O -L -J -k https://www.mpich.org/static/downloads/4.2.0rc1/mpich-4.2.0rc1.tar.gz      \
    --output $DIR/mpich-4.2.0rc1.tar.gz                                                                       \
    && tar -zxvf $DIR/mpich-4.2.0rc1.tar.gz -C $DIR/                         						   \
    && cd $DIR/mpich-4.2.0rc1/                     						                           \
    && ./configure --prefix=$DIR/mpich            									   \
    && make -j 8                                     									   \
    && make install

# Installing ZLIB LIBRARY
RUN cd $DIR/ 													  \
    && curl -O -L -J -k https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/zlib-1.2.11.tar.gz      \
    --output $DIR/zlib-1.2.11.tar.gz                                                                       \
    && tar -zxvf $DIR/zlib-1.2.11.tar.gz -C $DIR/                      						  \
    && cd $DIR/zlib-1.2.11/                        									  \
    && ./configure --prefix=$DIR/grib2            									  \
    && make -j 8                                      									  \
    && make install

# INSTALLING LIBPNG LIBRARY
RUN cd $DIR/													\
    && curl -O -L -J -k http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz \
    --output $DIR/libpng-1.2.50.tar.gz                                                                  \
    && tar -zxvf $DIR/libpng-1.2.50.tar.gz -C $DIR/                        						\
    && cd $DIR/libpng-1.2.50/                     									\
    && ./configure --prefix=$DIR/grib2            									\
    && make -j 8                                       									\
    && make install

# INSTALLING JASPER LIBRARY
RUN cd $DIR/ 													  \
    && curl -O -L -J -k http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/jasper-1.900.1.tar.gz  \
    --output $DIR/jasper-1.900.1.tar.gz                                                                   \
    && tar -zxvf $DIR/jasper-1.900.1.tar.gz -C $DIR/                                                                  \
    && cd $DIR/jasper-1.900.1/                    									  \
    && ./configure --prefix=$DIR/grib2            									  \
    && make                                       									  \
    && make install

# Install HDF5 using Make
RUN cd $DIR/												           \
    && curl -O -L -J -k https://www2.mmm.ucar.edu/people/duda/files/mpas/sources/hdf5-1.10.5.tar.bz2      \
    --output $DIR/hdf5-1.10.5.tar.bz2                                                                       \
    && tar -jxvf $DIR/hdf5-1.10.5.tar.bz2 -C $DIR/                         						   \
    && cd $DIR/hdf5-1.10.5/                     						                           \
    && ./configure --prefix=$DIR/hdf5 --with-zlib=$DIR/grib2 --enable-fortran --enable-shared            		   \
    && make -j 8                                       									   \
    && make install


# INSTALLING NETCDF LIBRARY
RUN cd ${DIR}                                                                                                     && \
    curl -O -L -J -k https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.9.2.tar.gz     \
    --output $DIR/netcdf-c-4.9.2.tar.gz                                                                            && \
    tar -zxvf $DIR/netcdf-c-4.9.2.tar.gz  -C $DIR/                        				         && \
    cd $DIR/netcdf-c-4.9.2                                                                 			 && \
    ./configure \
        CPPFLAGS="-I$DIR/hdf5/include" LDFLAGS="-L$DIR/hdf5/lib" LIBS="-lbsd" \
        --prefix=$DIR/netcdf --disable-dap --enable-netcdf-4 --enable-shared --disable-filter-testing  	 && \
    make -j 4                                                                                			 && \
    make install                               									  \
    && rm $DIR/*.gz

# # Installed latest NETCDF-Fortran
ENV LIBS="-lnetcdf -lhdf5_hl -lhdf5 -lz"
RUN cd $DIR/                                                                                                     && \
    curl -O -L -J -k https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/netcdf-fortran-4.5.2.tar.gz     \
    --output $DIR/netcdf-fortran-4.5.2.tar.gz                                                                            && \
    tar -zxvf $DIR/netcdf-fortran-4.5.2.tar.gz  -C $DIR/                        				         && \
    cd $DIR/netcdf-fortran-4.5.2 && \
    ./configure \
        CPPFLAGS="-I$DIR/hdf5/include" LDFLAGS="-L$DIR/hdf5/lib" LIBS="-lbsd" FCFLAGS="-fallow-argument-mismatch" \
       --prefix=$DIR/netcdf --disable-shared   			 && \
    make                                                                                 			 && \
    make install

# CONFIGURING  AND Compile WRFV4.5-DMPAR
# To compile a serial implementation use option 32, SMPAR option 33, DMPAR option 34

SHELL ["/bin/bash", "-c"]
RUN cd /pi-wrf/WRF_System/WRFV4.5.2/ \
    && ./configure <<< $'34\r1\1' \
    && sed -i 's/-lnetcdff -lnetcdf/-lnetcdff -lnetcdf -lbsd/g' configure.wrf \
    && ./compile em_real 2>&1 |& tee log.compile

# CONFIGURE & COMPILE WPS 4.5
RUN cd /pi-wrf/WRF_System/WPS/ \
    && ./configure

##----- Edits 6-20-2024------------##
# ADDING RESOURCES

ADD /resources/images/* /pi-wrf/WRF_System/lib/
ADD /resources/*.csv /pi-wrf/WRF_System/lib/
ADD /resources/ref_namelist.wps /pi-wrf/WRF_System/WPS/namelist.wps
ADD /resources/ref_namelist.input /pi-wrf/WRF_System/WRFV4.5.2/run/namelist.input
ADD /src/cleanwrf /pi-wrf/WRF_System/lib/
ADD /src/Plotting_Scripts/* /pi-wrf/WRF_System/lib/Plotting_Scripts/
ADD /src/pi-wrf/*.*  /pi-wrf/pi_wrf/pi_wrf/
ADD /src/pi-wrf/Pages/* /pi-wrf/pi_wrf/pi_wrf/Pages/
ADD /src/run_wrf /pi-wrf/

# CREATING DIRECTORY FOR JUPYTER NOTEBOOKS

RUN     mkdir -p /pi-wrf/src/notebooks
COPY    envs/smpar_gui/notebooks/* /pi-wrf/src/notebooks

##---------------------------------##

# Set the working directory
WORKDIR /pi-wrf/src/notebooks

# # Copy your local files into the containers working directory
# COPY . /app

# # Start an interactive shell with Python 3
# CMD ["/bin/bash"]

ENV TINI_VERSION v0.19.0

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
# ENTRYPOINT ["/bin/bash", "-c"]

# CMD ["jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

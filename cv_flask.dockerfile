# dockerfile for cv_flask
#
# - used OpenFace dockerfile https://github.com/leocnj/docker-images/blob/master/openface-cambridge/openface-cambridge.dockerfile
# - python
# - Flask
# - FFMPEG

FROM ubuntu:16.04
MAINTAINER Lei Chen <lei.chen@liulishuo.com>

# OpenFace
RUN apt-get update && \
	apt-get install -y \
	build-essential \
	checkinstall \
	clang-3.7 \
	clang++-3.7 \
	cmake \
	git \
	libavcodec-dev \
	libavformat-dev \
	libboost-all-dev \
	libc++abi-dev \
	libc++-dev \
	libdc1394-22-dev \
	libgtk2.0-dev \
	libjasper-dev \
	libjpeg-dev \
	liblapack-dev \
	libopenblas-dev \
	libpng-dev \
	libswscale-dev \
	libtbb2 \
	libtbb-dev \
	libtiff-dev \
	llvm \
	pkg-config \
	python-dev \
	python-numpy \
	sshfs \
	unzip \
	wget \
&&  rm -rf /var/lib/apt/lists/* 

# OpenCV 3.4.0
RUN wget https://github.com/opencv/opencv/archive/3.4.0.zip && \
	unzip 3.4.0.zip -d /opt && \
	cd /opt/opencv-3.4.0 && \
	mkdir build && \
	cd build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D WITH_TBB=ON -D BUILD_SHARED_LIBS=OFF .. && \
	make -j2 && \
	make install && \
    rm -r /opt/opencv-3.4.0 && \
    cd / && rm 3.4.0.zip

# OpenFace lastest
# RUN cd /opt && \
# 	git clone https://github.com/TadasBaltrusaitis/OpenFace.git && \
#   git is too slow; use zip 480MB
RUN wget https://github.com/TadasBaltrusaitis/OpenFace/archive/OpenFace_v1.0.0.zip && \
    unzip OpenFace_v1.0.0.zip -d /opt && \
    cd /opt/OpenFace-OpenFace_v1.0.0 && \
	mkdir build && \
	cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D WITH_TBB=ON -D BUILD_SHARED_LIBS=OFF .. && \
	make -j2 && \
	make install && \
    rm -r /opt/OpenFace-OpenFace_v1.0.0 && \
    cd / && rm OpenFace_v1.0.0.zip


# set working directory
# WORKDIR /opt/OpenFace/build/bin
# python flask, FFMPEG
RUN apt-get update && \
    apt-get install -y python-pip python-dev && \
    pip install Flask && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:djcj/hybrid && \
    apt-get install -y ffmpeg && \
    apt-get remove -y python-dev python-pip && \
    rm -rf /var/lib/apt/lists/*  

###################################################################
# Flask App
COPY . /App

WORKDIR /App

# Make port 80 available to the world outside this container
EXPOSE 80

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
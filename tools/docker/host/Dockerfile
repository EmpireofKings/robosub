FROM ros:kinetic

RUN apt-get update && apt-get install -y \
    ros-kinetic-mavros \
    ros-kinetic-cv-bridge \
    ros-kinetic-image-transport \
    clang-format \
    pylint

ADD install-cuda.sh /install-cuda.sh 
RUN /install-cuda.sh

ADD install-zed.sh /install-zed.sh
RUN /install-zed.sh
RUN apt-get update && apt-get install -y ros-kinetic-tf2-geometry-msgs ros-kinetic-pcl*

VOLUME catkin_ws
WORKDIR /catkin_ws
CMD ["catkin_make"]

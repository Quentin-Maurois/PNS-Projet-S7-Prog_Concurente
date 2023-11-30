#!/bin/bash

#docker run heat_diffusion:3

xhost +local:docker
docker run --rm -it --network host -e DISPLAY=$DISPLAY heat_diffusion:3
xhost -local:docker

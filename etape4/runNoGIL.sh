#!/bin/bash

xhost +local:docker
docker run --rm -it --network host -e DISPLAY=$DISPLAY heat_diffusion:4
xhost -local:docker

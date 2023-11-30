#!/bin/bash

### docker build the project that consumes too much RAM
#docker image rm -f heat_diffusion:3
#docker build -t heat_diffusion:3 -f ./Dockerfile_1 .

### docker build the project with the correct implementation
docker image rm -f heat_diffusion:3.1
docker build -t heat_diffusion:3.1 -f ./Dockerfile_2 .
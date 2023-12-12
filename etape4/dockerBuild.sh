#!/bin/bash

### docker build the project with the correct implementation
docker image rm -f heat_diffusion:4
docker build -t heat_diffusion:4 -f ./Dockerfile .

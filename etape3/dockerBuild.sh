#!/bin/bash


docker image rm -f heat_diffusion:3
docker build -t heat_diffusion:3 -f ./Dockerfile_1 .

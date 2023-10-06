#!/bin/bash


docker image rm -f pythonsansgil:deuxsinglethreads
docker image rm -f pythonsansgil:deuxthreadslecturepartagee
docker image rm -f pythonsansgil:racecondition

docker build -t pythonsansgil:deuxsinglethreads -f ./Dockerfile_deuxSingleThreads .
docker build -t pythonsansgil:deuxthreadslecturepartagee -f ./Dockerfile_deuxThreadsLecturePartagee .
docker build -t pythonsansgil:racecondition -f ./Dockerfile_raceCondition .


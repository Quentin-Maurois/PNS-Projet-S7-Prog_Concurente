#!/bin/bash


echo ---avec gil---
echo deux threads sans connexion entre eux :
python deuxSingleThreads.py
echo deux threads avec lecture d une variable partagee en lecture :
python deuxThreadsLecturePartagee.py
echo deux threads avec lecture et ecriture d une variable partagee :
python exampleRaceCondition.py


echo ---sans gil---
echo deux threads sans connexion entre eux :
docker run pythonsansgil:deuxsinglethreads
echo deux threads avec lecture d une variable partagee en lecture :
docker run pythonsansgil:deuxthreadslecturepartagee
echo deux threads avec lecture et ecriture d une variable partagee :
docker run pythonsansgil:racecondition

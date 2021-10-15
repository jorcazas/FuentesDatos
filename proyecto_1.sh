#!/bin/bash

if [[ ! -e estaciones.xml ]]
then
 wget https://bit.ly/2V1Z3sm
 mv 2V1Z3sm estaciones.xml
fi

if [[ ! -e precios.xml ]]
then
 wget https://bit.ly/2JNcTha
 mv 2JNcTha precios.xml
fi

bash proyecto_1_transform_1.sh precios.xml

bash proyecto_1_transform_2.sh estaciones.xml

bash proyecto_1_load.sh

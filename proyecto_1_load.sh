#!bin/bash

psql -f updload.sql service=fuentes_datos
psql -c '\copy raw.precios from precios.csv with csv header;' service=fuentes_datos
psql -c '\copy raw.estaciones from estaciones.csv with csv header;' service=fuentes_datos

drop schema if exists raw cascade;
create schema raw;
drop table if exists raw.estaciones;
create table raw.estaciones(
id_estacion int constraint pk_id_estacion primary key,
nombre varchar(50),
latitud float,
longitud float
);
drop table if exists raw.precios;
create table raw.precios(
estacion_servicio int constraint pk_estacion_servicio primary key,
regular float,
premium float,
diesel float
);

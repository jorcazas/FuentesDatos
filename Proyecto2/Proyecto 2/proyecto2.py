# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 16:39:57 2021

@author: javi2
"""

import psycopg2
import yaml
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
#%%
def read_yaml_file(yaml_file):
    """ load yaml cofigurations """

    config = None
    try:
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
    except:
        raise FileNotFoundError('Couldnt load the file')

    return config

def get_db_conn(creds_file):
    """ Get an authenticated psycopg db connection, given a credentials file"""
    creds = read_yaml_file(creds_file)['db']

    connection = psycopg2.connect(
        user=creds['user'],
        password=creds['pass'],
        host=creds['host'],
        port=creds['port'],
        database=creds['db']
    )

    return connection

#%%
#1. 
#Ocupa la función get_db_conn() a través de la cuál obtenemos una conexión a la 
#BD (postgres) con psycopg2 leyendo del archivo credentials.yaml (utilizando la 
#función read_yaml()) las credenciales de acceso a la BD.

root="C:\\Users\\javi2\\Documents\\Fuentes de Datos\\Proyecto 2\\"
creds=root+"conf\\credentials.yaml"
db_conn = get_db_conn(creds)

#2. 
#Genera un query sql en donde obtengas el id_estacion, nombre, longitud, latitud, 
#regular, preimum, diesel de todos los precios. <- Necesitarás un inner join.
query="""select e.id_estacion, e.nombre, e.longitud, e.latitud, p.regular, p.premium, p.diesel 
from raw.estaciones e inner join raw.precios p on e.id_estacion = p.estacion_servicio;
"""

data = pd.read_sql(query, db_conn)
#%%%

#En Pandas
#Utilizando shape, cuántas observaciones tienes.
print("Tengo " + str(data.shape[0]) + " observaciones")

#Utilizando is.na():
    
#cuántas estaciones no tienen gasolina regular
print(data['regular'].isna().sum())
#cuántas estaciones no tienen gasolina premium
print(data['premium'].isna().sum())
#cuántas estaciones no tienen gasolina diesel
print(data['diesel'].isna().sum())
#cuántas estaciones solo tienen gasolina regular
print(data[(data['premium'].isna()) & (data["diesel"].isna())].id_estacion.count())
#cuántas estaciones solo tienen gasolina regular y premium
print(data[(data['regular'].notna()) & (data["premium"].notna()) & (data["diesel"].isna())].id_estacion.count())
#cuántas estaciones solo tienen gasolina regual y diesel
print(data[(data['regular'].notna()) & (data["diesel"].notna()) & (data["premium"].isna())].id_estacion.count())

#qué estaciones (nombre) dieron gasolina premium "gratis" de acuerdo a los datos.
print("Las estaciones que dieron gasolina premium 'gratis' de acuerdo a los datos son:")
print(data[data['premium']==0.0].nombre)

#Cuántas estaciones de gasolina venden de los 3 tipos de gasolina.
aux=data[['diesel', 'premium', 'regular']].dropna() 
print(str(aux.shape[0])+" estaciones venden de los 3 tipos de gasolina")

#%%
#3. 
#En el data frame generado agrega dos nuevas columnas: lat y lon.
#Para lat deberás convertir la columna latitud a ese valor en una escala del 10 al 99. 
#Por ejemplo: si tienes el valor 999999 deberá quedar como 99.9999, si tienes 
#el valor 20 deberá quedar como 20.

lat=[]
for element in data["latitud"]:
    raw=str(element).replace(".", "")
    lat.append(raw[:2]+"."+raw[2:])
data["lat"]=pd.Series(lat, name="lat")
    
#%%
#Para lon deberás convertir la columna longitud a ese valor en negativo y debe 
#estar en el rango de 99 al 120. Si la longitud inicia con 1 deberás dejarlo 
#como "cientos", en otro caso dejar con dos valores enteros. 
#Por ejemplo, si tienes el valor 99999 deberá quedar como -99.999, si tienes 
#el valor 102333 deberá quedar como -102.333.
lon=[]
for element in data["longitud"]:
    raw=str(element).replace("-", "").replace(".", "")
    if(raw[0]=="1"):
        lon.append("-"+raw[:3]+"."+raw[3:])
    else:
        lon.append("-"+raw[:2]+"."+raw[2:])
data["lon"]=pd.Series(lon, name="lon")

#%%
#Elimina las columnas latitud y longitud en el mismo data frame.
data.drop(["latitud", "longitud"], axis=1, inplace=True)
#%%
#Genera un describe(). Interpreta el significado de cada métrica en el describe 
#para las columnas regular, premium, diesel.
print(data.describe())
print("""Mean: Podemos observar que en promedio, la gasolina premium es más
      cara que las otras dos en todas las gasolineras. \n Std: De igual manera, 
      la desviación estándar de los precios es mayor en la gasolina premium, lo que
      nos indica que su precio fluctúa más que el de las otras gasolinas; el precio
      del diesel es el que menos varía, lo cual puede deberse a que su precio debe 
      ser más estable pues de él dependen los medios de transporte pesados, es decir,
      de él dependen los precios de muchos otros bienes. Por otro lado, la gasolina
      premium puede ser la que menos demanda tenga, lo que significa que las fluctuaciones
      en el precio no tienen un impacto tan grande en la economía, de ahí que su desviación 
      estándar sea mayor. \n Min y Max: Estos representan el precio más bajo y el
      más alto registrado en las gasolineras; curiosamente, en premium y diesel 
      hay un mínimo de $0, lo cual significa que hubo gasolineras que probablemente
      regalaron estos dos tipos de gasolina, o fue un error de registro. En cuanto
      al máximo, el precio más alto fue de diesel, mientras que la regular mantuvo 
      el máximo más bajo de las tres. \n Cuartiles: Por úlitmo, los cuartiles nos 
      muestran cómo se distribuyen los precios de las gasolinas: en el primer cuartil
      (25%) se encuentra un cuarto de los precios de gasolinas, es decir, un cuarto
      de las gasolineras dieron precios menores a $19.75 para regular, a $21.88 para premium
      y a $21.15 para diesel; la mitad de las gasolineras dio precios menores
      a $20.29 (regular), $22.45 (premium), $21.76 (diesel); y 3 cuartos de las 
      gasolineras dieron precios menores a $20.99 (regular), $22.99 (premium), $22.29 (diesel)
      
      """)

#%%
#Cuál es la estación de gasolina -nombre y coordenadas- con el precio más caro de gasolina regular
print(data[data["regular"]==data.regular.max()][["nombre", "lon", "lat"]])
#Cuál es la estación de gasolina -nombre y coordenadas- con el precio más caro de gasolina premium
print(data[data["premium"]==data.premium.max()][["nombre", "lon", "lat"]])
#Cuál es la estación de gasolina -nombre y coordenadas- con el precio más caro de gasolina diesel
print(data[data["diesel"]==data.diesel.max()][["nombre", "lon", "lat"]])
#Cuál es la estación de gasolina -nombre y coordenadas- con el precio más barato de gasolina regular
print(data[data["regular"]==data.regular.min()][["nombre", "lon", "lat"]])
#Cuál es la estación de gasolina -nombre y coordenadas- con el precio más barato de gasolina premium
print(data[data["premium"]==data.premium.min()][["nombre", "lon", "lat"]])
#Cuál es la estación de gasolina -nombre y coordenadas- con el precio más barato de gasolina diesel
print(data[data["diesel"]==data.premium.min()][["nombre", "lon", "lat"]])


#%%
#4.
#Debido a que estamos en CDMX -> verifica las latitudes y longitudes posibles 
#de la CDMX <-, ¿a qué estación de gasolina -nombre y coordenadas- deberíamos 
#ir a llenar el tanque para cada tipo de gasolina? (no importa la distancia)
cdmx={"latmin":19.05, "latmax":19.6,  "lonmin":-99.36, "lonmax":-98.95}
#gasolineras en cdmx para regular
gas_en_cdmx=data[(data["lat"]>cdmx["latmin"]) & (data["lat"]<cdmx["latmax"])\
                 & (data["lon"]>cdmx["lonmin"]) & (data["lon"]<cdmx["lonmax"])]
gcdmx_regular=gas_en_cdmx
print(gas_en_cdmx[["nombre", "lon", "lat"]])



#De este subconjunto, genera un data frame que nos diga ¿cuántas estaciones de 
#gasolina venden cada tipo de gasolina? Toma el tipo de gasolina como independiente, 
#es decir, una estación puede vender de las 3 gasolinas, en este caso aparacerá 
#en cada conteo, tanto para el regular como para el premium como para el diesel.


#%%
#5.
#Genera un nuevo data frame que junte las columnas regular, premium, diesel en 
#dos nuevas columnas: tipo_gasolina y precio, la primera se llena con el tipo 
#de gasolina: regular, premium, diesel y la segunda con el valor correspondiente al precio.
data_tipo_gasolina = data.melt(id_vars='id_estacion', value_vars=["regular", "premium", "diesel"]\
                               , var_name="tipo_gasolina", value_name="precio")
print(data_tipo_gasolina)

#Utilizando shape, cuantas observaciones tienes.
#Genera un describe(). Interpreta el significado de cada métrica en el describe 
#para la columna precio. ¿Cómo cambian las estadísticas?
print("Tengo " + str(data_tipo_gasolina.shape[0]) + " observaciones")

print(data_tipo_gasolina.describe())
print("""Mean: Podemos observar que ahora sólo tenemos un promedio que junta todos
      los precios de todas las gasolineras, el cual es $21.29. A diferencia de 
      las estadísticas anteriores, aquí perdemos información con respecto a los precios
      de cada tipo de gasolina. \n Std: De igual manera, la desviación estándar
      ahora se calcula para el total de los precios, por lo que no podemos saber 
      con certeza la situación de las gasolinas en particular.\n Min y Max: Estos 
      representan el precio más bajo y el más alto registrado en todas las gasolineras; 
      también aquí aparece el mínimo de $0 y el máximo es el máximo de los máximos
      registrados en las estadísticas anteriores, es decir, $29.29. \n Cuartiles: Por 
      úlitmo, los cuartiles también nos muestran cómo se distribuyen los precios, pero
      esta vez es la distribución de todas los precios de todas las gasolinas: en el primer cuartil
      (25%) se encuentra un cuarto de los precios de gasolinas, es decir, un cuarto
      de todas las gasolineras dieron precios menores a $20.42, aunque no podemos
      saber con certeza si se trata de regular, premium o diesel, o las tres; 
      la mitad de las gasolineras dio precios menores
      a $21.50; y 3 cuartos de las gasolineras dieron precios menores a $22.39 \n
      Como podemos observar, en este caso, tener las estadísticas de los datos 
      acomodados de esta manera (formato long) nos da mucha menos información que 
      cuando los tenemos en un formato wide.
      
      """)

#%%
#6.
#De la pegunta 5. Genera un boxplot (en una sola gráfica) que contenga las distribuciones 
#de los 3 tipos de gasolina. Agrega el promedio. Recuerda poner nombres a los ejes 
#y unidades (si aplica). Cada tipo de gasolina debe estar en un color diferente. 
#Interpreta la gráfica, cuál consideras que es el insight más interesante.
a = sns.boxplot(data=data_tipo_gasolina, x="tipo_gasolina", y="precio", showmeans=True)
a.set_title("Distribuciones de los precios de las gasolinas")
a.set_xlabel("Tipo de gasolina")
a.set_ylabel("Precio en pesos mexicanos ($)")
plt.show()
print("")

#%%
#De la pregunta 5. Genera un solo histograma (en una sola gráfica) con los precios 
#que incluya la distribución de cada tipo de gasolina. Incluye un parámetro alpha 
#que te permita agregar transparencia para que se vean las 3 distribuciones en la 
#misma gráfica. Cada tipo de gasolina va de color diferente.
a = sns.histplot(data=data_tipo_gasolina, x="precio", hue="tipo_gasolina")
a.set_title("Histograma de distribuciones de precios")
plt.show()



#%%
#Genera un mapa que muestre las estaciones de las que tienes registros. ¿Existen 
#estaciones que no están en México? En caso afirmativo, ¿cuántas, qué crees que
#haya pasado? 
fig=px.scatter_geo(data_frame=data,lon=data["lon"], lat=data["lat"])
fig.show()

#Genera un mapa que muestre las estaciones que venden regular. ¿Existen estaciones 
#que no están en México? En caso afirmativo, ¿cuántas, qué crees que haya pasado?

#Genera un mapa que muestre las estaciones que venden premium. ¿Existen estaciones 
#que no están en México? En caso afirmativo, ¿cuántas, qué crees que haya pasado?

#Genera un mapa que muestre las estaciones que venden diesel. ¿Existen estaciones 
#que no están en México? En caso afirmativo, ¿cuántas, qué crees que haya pasado?



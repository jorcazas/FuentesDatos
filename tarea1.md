## Tarea 1
Para esta tarea, se descargó el archivo first 5k.csv.zip de la url https://www.dropbox.com/s/zlb4zr3xwcwkyn7/first_5k.csv.zip?dl=0 y se descomprimió en un archivo llamado tarea1.csv

A continuación, se muestran los ejercicios hechos sobre este archivo, por bloques de código, en el siguiente formato:

~~~
Pregunta

Línea de código que responde a la pregunta

Salida obtenida de la línea de código
~~~
### Ejercicios

~~~
1. ¿Cuántas líneas tiene el archivo? (el resultado contempla también la primera línea del archivo, es decir, la línea que contiene los nombres de las columnas; para saber sólo la cantidad de registros del archivo, al resultado se le resta 1)

wc -l tarea1.csv

5432123 tarea1.csv
~~~

~~~
2. ¿Cuántos registros tienen la palabra soriana? (Toma en cuenta que la mayoría de los registros están en mayúsculas, ¡pero no todos!). Aquí asumo que buscamos sólo los registros con la palabra 'soriana' y omitimos todos los que tengan palabras que tienen el patrón 'soriana' dentro.

grep -ciE '\"\s?soriana\s?\"|\ssoriana\"?\s|\"\s?soriana\s' tarea1.csv

965694
~~~


~~~
3. ¿Cuántos registros tienen la palabra tortilla? (Mismas recomendaciones que el punto 4). Aquí asumo que buscamos sólo los registros con la palabra 'tortilla' y omitimos todos los que tengan palabras que tienen el patrón 'tortilla' dentro, como 'tortillas'

grep -ciE '\"\s?tortilla\s?\"|\stortilla\"?\s|\"\s?tortilla\s' tarea1.csv

56436
~~~

~~~
4. De los registros que tienen la palabra tortilla, ¿de qué estado de la república es el 13vo último elemento y cuál es el precio? (Regresa solo el 13vo último elemento y verifica el estado y el precio, ponlo el palabras)

grep -iE '\"\s?tortilla\s?\"|\stortilla\"?\s|\"\s?tortilla\s' tarea1.csv | tail -13 | head -1

"TORTILLA DE MAIZ","1 KG. GRANEL","S/M","TORTILLAS Y DERIVADOS DEL MAIZ","BASICOS",7.5,"2011-11-28 00:00:00.000","COMERCIAL MEXICANA","TORTILLERIA","COMERCIAL MEXICANA","JUAN PABLO II","MÉXICO","TOLUCA                                  ",NA,NA

Estado: Estado de México
Precio: 7.5 pesos
~~~

~~~
5. ¿Cuántos registros tienes que sean de la categoría juguetes del estado quintana roo y que sean hot wheels?

grep -iE '\"\s?juguetes\s?\"|\sjuguetes\"?\s|\"\s?juguetes\s' tarea1.csv | grep -iE '\"quintana roo\"' | grep -ciE 'hot wheels'

116
~~~

~~~
6. ¿Cuántos registros de tiendas de autoservicio tienes tienda de autoservicio?

grep -ciE '\"tienda de autoservicio\"' tarea1.csv

4547966
~~~

~~~
7. ¿Cuántos registros de papelerías tienes papeleria?

grep -ciE 'papeler[i|í]a' tarea1.csv

154667
~~~

~~~
8. ¿Cuántos registros de tortillería tienes tortilleria?

grep -ciE 'tortiller[i|í]a' tarea1.csv

33038
~~~

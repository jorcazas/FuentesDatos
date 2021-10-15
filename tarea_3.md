~~~
1.

wget https://archivo.datos.cdmx.gob.mx/casos_nacionales_covid-19.csv

mv casos_nacionales_covid-19.csv casos_covid.csv
~~~

~~~
2.

awk -F, '{print tolower($0)}' casos_covid.csv > casos_covid_min.csv
~~~

~~~
3.

awk -F, '{
  gsub(/á/, "a")
  gsub(/é/,"e")
  gsub(/í/, "i")
  gsub(/ó/, "o")
  gsub(/ú/, "u")
  print $0}' casos_covid_min.csv > casos_covid_min_sa.csv

mv casos_covid_min_sa.csv casos_covid.csv
~~~

~~~
4. ¿Cuántas personas fallecieron menores de 20 años? [0-19]


awk -F, '{
  if ($14 !~ "na" && $17 !~ "edad" && ($17 <= 19))
   sum+=1
  }
  END {
    print(sum)
  }' casos_covid.csv

494
~~~

~~~
5. ¿Cuántas personas embarazadas fallecieron entre julio y diciembre del 2020? (Revisa la operación ~ en los condicionales awk).


awk -F, '{
  if ($19 !~ "no aplica" && $19 !~ "no" && $14 ~ "2020-0[7-9]|2020-1[0-2]")
   sum+=1
  }END{
    print(sum)
    }' casos_covid.csv

9
~~~

~~~
6. De las personas entre 30 y 50 [30-50] años que fallecieron, ¿cuántas tenían diabetes?


awk -F, '{
  if ($14 !~ "na" && $17 !~ "edad" && ($17 >= 30) && ($17 <= 50) && $22 ~ "si")
    sum+=1
  }END{
    print(sum)
    }' casos_covid.csv

2663
~~~

~~~
7. De las personas que encontraste en la pregunta 6, ¿cuántas no residen en la "MICHOACÁN"?


awk -F, '{
  if ($14 !~ "na" && $17 !~ "edad" && ($17 >= 30) && ($17 <= 50) && $22 ~ "si" && $9 !~ "michoacan")
    sum+=1
  }END{
    print(sum)
  }' casos_covid.csv

2663
~~~

~~~
8. ¿Cuántas personas menores de 19 años [0-18] fallecieron en agosto del 2021?


awk -F, '{
  if($14 !~ "na" && $17 < 19 && $14 ~ "2021-08")
    sum++
  }END{
    print(sum)
  }' casos_covid.csv

33
~~~

~~~
9. Verifica si la columna de fecha de defunción tiene una longitud de 10 caracteres. En caso de que no sea verifica si tiene números, de no ser así, imprime el siguiente mensaje El renglón <NR> no tiene asociada una fecha <$fecha_def>; si contiene números verifica que inicien con 2020 e imprime El renglón <NR> no tiene el formato adecuado de fecha <$fecha_def>.


awk -F, '{
  if(length($14) != 10){
    if($14 ~ "2020")
      print "El renglón ", NR, " no tiene el formato adecuado de fecha ", $14
    else
      print "El renglón ", NR, " no tiene asociada una fecha ", $14
  }
}' casos_covid.csv
~~~

~~~
10. Cuenta cuántos registros de fallecidos tenemos de cada entidad de residencia.


awk -F, '{
  if($14 != "na")
    arr[$9]++
  }END{
    for (e in arr)
      print "Entidad de residencia: ", e, "; registros: ", arr[e]
  }' casos_covid.csv


Entidad de residencia:  "sonora" ; registros:  6
Entidad de residencia:  "michoacan de ocampo" ; registros:  74
Entidad de residencia:  "san luis potosi" ; registros:  20
Entidad de residencia:  "entidad_res" ; registros:  1
Entidad de residencia:  "tabasco" ; registros:  4
Entidad de residencia:  "hidalgo" ; registros:  481
Entidad de residencia:  "veracruz de ignacio de la llave" ; registros:  104
Entidad de residencia:  "zacatecas" ; registros:  5
Entidad de residencia:  "tlaxcala" ; registros:  69
Entidad de residencia:  "nuevo leon" ; registros:  11
Entidad de residencia:  "nayarit" ; registros:  2
Entidad de residencia:  "jalisco" ; registros:  11
Entidad de residencia:  "quintana roo" ; registros:  12
Entidad de residencia:  "queretaro" ; registros:  50
Entidad de residencia:  "guanajuato" ; registros:  57
Entidad de residencia:  "sinaloa" ; registros:  6
Entidad de residencia:  "guerrero" ; registros:  169
Entidad de residencia:  "yucatan" ; registros:  5
Entidad de residencia:  "tamaulipas" ; registros:  18
Entidad de residencia:  "morelos" ; registros:  158
Entidad de residencia:  "puebla" ; registros:  268
Entidad de residencia:  "oaxaca" ; registros:  78
Entidad de residencia:  na ; registros:  50338
Entidad de residencia:  "mexico" ; registros:  15505

~~~
~~~
11. Cuenta cuántos registros tenemos de cada sector diferente, imprime:


awk -F, '{
  if(NR > 1)
    arr[$5]+=1
  }END{
    for (e in arr)
      print "Sector: ", e, "; registros: ", arr[e]
  }' casos_covid.csv

Sector:  "municipal" ; registros:  1
Sector:  "cruz roja" ; registros:  642
Sector:  "sedena" ; registros:  13562
Sector:  "imss" ; registros:  477688
Sector:  "issste" ; registros:  40426
Sector:  "dif" ; registros:  3
Sector:  "privada" ; registros:  136634
Sector:  "semar" ; registros:  6189
Sector:  "pemex" ; registros:  14382
Sector:  "universitario" ; registros:  23
Sector:  "estatal" ; registros:  1460
Sector:  "imss-bienestar" ; registros:  65
Sector:  na ; registros:  36
Sector:  "ssa" ; registros:  3298483
~~~

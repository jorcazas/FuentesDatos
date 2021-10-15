#!/bin/bash
header="id_estacion,nombre,latitud,longitud"
estaciones=$1

if [[ -e estaciones.csv ]]
then
 rm estaciones.csv
fi

touch estaciones.csv
echo $header >> estaciones.csv

if [[ -e estaciones_sin_encoding.txt ]]
then
 rm estaciones_sin_encoding.txt
fi

touch estaciones_sin_encoding.txt
sed '1d;2d' $estaciones > estaciones_sin_encoding.txt #borramos las primeras dos líneas porque no nos sirven para separar los datos como queremos
sed -i '1 i </place>' estaciones_sin_encoding.txt


awk 'BEGIN {RS = "</place>"}
           {FS = "<[a-z]+"}
           {

             gsub(/[\.|,|\-]/,"",$3)

             if(match($2, /id/)){
               print id","nom","lat","lon
               match($2, /[0-9]+/)
               id=substr($2, RSTART, RLENGTH)
               nom=""
               lat=""
               lon=""
             }
             if(match($3, /name/)){
               match($3, />.*</)
               nom_=substr($3,RSTART, RLENGTH)
               len=length(nom_)
               nom=substr(nom_,2,len-2)
             }
             if(match($6, /x\>/)){
               match($6, /-?[0-9]+\.[0-9]+/)
               lon=substr($6,RSTART, RLENGTH)
             }

             if(match($7, /y>/)){
               match($7, /-?[0-9]+\.[0-9]+/)
               lat=substr($7,RSTART, RLENGTH)
             }
           }
           END{
             print id","nom","lat","lon
           }' estaciones_sin_encoding.txt >> estaciones.csv

sed -i '2d' estaciones.csv

#Con sed cambiar a minúsculas el contenido del atributo name (sin crear otro archivo).
sed -ie 's/\(.*\)/\L\1/g' estaciones.csv
#Con sed elimina los acentos del contenido del atributo name (sin crear otro archivo).
sed -ie 'y/ÁÉÍÓÚáéíóú/AEIOUaeiou/' estaciones.csv
#Con sed elimina signos de puntuación del atributo name (sin crear otro archivo). Signos de puntuación: ,;.:-. Por ejemplo: estacion rael, s. de r.l. de c.v. quedaría como estacion rael s de rl de cv
sed -ie 's/[\:|\;]//g' estaciones.csv #el . la , y el - se quitaron en pasos anteriores porque aquí afectaría a las coordenadas (línea 26)

#Con AWK averigua ¿De cuántas estaciones diferentes tienes geolocalización? Imprimir en terminal estaciones diferentes: <n>
#primero quitamos el header para no contarlo
cuantas=$(sed '1d' estaciones.csv | awk -F, '{
  if($3 != "" && $4 != ""){
    if($3 != ""){
      y[$1]=$3
    }else{
      y[$1]=""
    }
    if($4 != ""){
      x[$1]=$4
    }else{
      x[$1]=""
    }
  }
}END{
  for(i in y){
    c+=1
  }
  print c
}')

echo "estaciones diferentes:" $cuantas

 #quitamos los archivos temporales que usamos
rm estaciones_sin_encoding.txt

if [[ -e estaciones.csve ]]
then
  rm estaciones.csve #no tengo idea por qué se genera una copia de estaciones.csv pero con extensión .csve, por eso lo borro
fi

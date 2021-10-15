#!/bin/bash
precios=$1

header="estacion_servicio,regular,premium,diesel"

if [[ -e precios.csv ]]
then
 rm precios.csv
fi

touch precios.csv
echo $header >> precios.csv

if [[ -e precios_sin_encoding.txt ]]
then
 rm precios_sin_encoding.txt
fi

touch precios_sin_encoding.txt
sed '1d;2d' $precios > precios_sin_encoding.txt #borramos las primeras dos líneas porque no nos sirven para separar los datos como queremos
sed -i '1 i </place>' precios_sin_encoding.txt


awk 'BEGIN {RS = "</place>"}
           {FS = "<[a-z]+"}
           {
              if(match($2, /id/)){

                print id","reg","prem","dies

                match($2, /[0-9]+/)
                id=substr($2, RSTART, RLENGTH)
                reg=""
                prem=""
                dies=""

              }
              if(match($3, /regular/)){
                match($3, /[0-9]+.[0-9]+/)
                reg=substr($3,RSTART, RLENGTH)
              }
              else if(match($3, /premium/)){
                match($3, /[0-9]+.[0-9]+/)
                prem=substr($3,RSTART, RLENGTH)
              }
              else if(match($3, /diesel/)){
                match($3, /[0-9]+.[0-9]+/)
                dies=substr($3,RSTART, RLENGTH)
              }
              if(match($4, /regular/)){
                match($4, /[0-9]+.[0-9]+/)
                reg=substr($4,RSTART, RLENGTH)
              }
              else if(match($4, /premium/)){
                match($4, /[0-9]+.[0-9]+/)
                prem=substr($4,RSTART, RLENGTH)
              }
              else if(match($4, /diesel/)){
                match($4, /[0-9]+.[0-9]+/)
                dies=substr($4,RSTART, RLENGTH)
              }
              if(match($5, /regular/)){
                match($5, /[0-9]+.[0-9]+/)
                reg=substr($5,RSTART, RLENGTH)
              }
              else if(match($5, /premium/)){
                match($5, /[0-9]+.[0-9]+/)
                prem=substr($5,RSTART, RLENGTH)
              }
              else if(match($5, /diesel/)){
                match($5, /[0-9]+.[0-9]+/)
                dies=substr($5,RSTART, RLENGTH)
              }

            }
            END{
              print id","reg","prem","dies
            }' precios_sin_encoding.txt >> precios.csv

sed -i '2d' precios.csv


#Con grep averigua ¿Cuántas gasolineras sirven gasolina regular en este conjunto de datos? Imprime en terminal gasolineras que sirven gasolina regular: <z>
gas_regular=$(grep -cE '^[0-9]+\,[0-9]+\.[0-9]+' precios.csv)
echo 'gasolineras que sirven gasolina regular:' $gas_regular
#Con grep averigua ¿Cuántas gasolineras sirven gasolina diesel en este conjunto de datos? Imprime en terminal gasolineras que sirven gasolina diesel: <y>
gas_diesel=$(grep -cE '[0-9]$' precios.csv)
echo 'gasolineras que sirven gasolina diesel:' $gas_diesel
#Con grep averigua ¿Cuántas gasolineras sirven premium en este conjunto de datos? Imprime en terminal gasolineras que sirven gasolina premium: <x>
gas_premium=$(grep -cE '([0-9]+\,[0-9]*)$' precios.csv)
echo 'gasolineras que sirven gasolina premium:' $gas_premium
#Con AWK averigua ¿De cuántas gasolineras diferentes tienes datos de precios? * Te puedes apoyar de un archivo auxiliar creado con grep o sed. Imprime en terminal gasolineras diferentes: <m>
awk -F, '{
  if($2 != ""){
    reg[$1]=$2
  }else
  {
    reg[$1]=""
  }
  if($3 != ""){
    prem[$1]=$3
  }else {
    prem[$1]=""
  }
  if($4!=""){
    dies[$1]=$4
  }else{
    dies[$1]=""
  }

}END{
  for (i in reg) {
    print "id"i "reg"reg[i], "prem"prem[i], "dies"dies[i]
  }
}' precios.csv > temp_cuantos.csv


cuantos=$(awk -F, '{
  c+=1
}END{
  print c
}' temp_cuantos.csv)

echo 'gasolineras diferentes:' $cuantos


#¿Cuántos renlgones de precios de gasolina tienes (una vez que ya tienes 1 renglón por estación de gasolina)? Imprime en terminal observaciones de precios: <n>
#usamos el archivo temporal de la pregunta pasada
cuantos=$(wc -l temp_cuantos.csv | grep -o '[0-9]*')
echo "observaciones de precios:" $cuantos

#quitamos los archivos temporales que usamos
rm temp_cuantos.csv
rm precios_sin_encoding.txt


~~~
1. Con wget o curl baja el archivo de nombres desde 1880 hasta 2014 de censos de Estados Unidos de la siguiente URL:https://www.dropbox.com/s/ezrp0t7uwyg7vgi/NationalNames.zip?dl=0

wget -O national_names.zip https://www.dropbox.com/s/ezrp0t7uwyg7vgi/NationalNames.zip?dl=0
~~~

~~~
2. Descomprime el archivo con unzip

unzip national_names.zip
~~~

~~~
3. Cambia el nombre del archivo a census_names.csv

mv NationalNames.csv census_names.csv

~~~

~~~
4. Modifica los nombres de las columnas para que estén todas en minúsculas.

sed -i -E '1s/([A-Z])/\L&/g' census_names.csv
~~~

~~~
5. Anna o Ana
a. ¿Cuántos registros hay que tenga el nombre Anna o Ana?

grep -iEc ',Anna,|,Ana,' census_names.csv

447

b. Modifica los registros que tengan Anna o Ana por el que aparezca más veces (imputación), es decir, si Anna aparece más veces que Ana entonces hay que cambiar las Ana por Anna -> Respeta la mayúscula inicial.

grep -iEc ',Ana,' census_names.csv

180

grep -iEc ',Anna,' census_names.csv

267

Modificamos entonces por 'Anna', ya que aparece 267 veces

sed -i 's/,Ana,/,Anna,/g' census_names.csv


c. Verifica que tienes el mismo número de registros para ahora todas las Anna o Ana

grep -c ',Anna,' census_names.csv

447
~~~

~~~
6. Emma o Ema
a. ¿Cuántos registros hay que tenga el nombre Emma o Ema?

grep -iEc ',Emma,|,Ema,' census_names.csv

364

b. Modifica los registros que tengan Emma o Ena por el que aparezca más veces (imputación), es decir, si Emma aparece más veces que Ema entonces hay que cambiar las Ema por Emma -> Respeta la mayúscula inicial.

grep -iEc ',Emma,' census_names.csv

246

grep -iEc ',Ema,' census_names.csv

118

Modificamos entonces por 'Emma', ya que aparece 246 veces

sed -i 's/,Ema,/,Emma,/g' census_names.csv

c. Verifica que tienes el mismo número de registros para ahora todas las Emma o Ema

grep -c ',Emma,' census_names.csv

364
~~~

~~~
7. Kateleen o Katilynn o Katelyn o Katelynn o Katelin o Katelynne o Katelyne o Katelinn o Katelyn

a. ¿Qué implicación consideras relevante en hacer estos cambios en los nombres? Considera que estamos tratando con datos de un censo.

Considero que cambiar registros siempre tendrá consecuencias negativas cuando se trate de analizar los resultados, sobre todo si son modificaciones tan importantes como cambiar un nombre. Aunque el cambio parezca insignificante, ya que sólo se están homogeneizando para tener mejor "control" sobre los datos, se trata de un falseamiento de la realidad y una reducción de la amplia gama de historias que se cuentan a través de los nombres. La manera en la que se escriben los nombres puede arrojar información valiosa sobre sus portadores y su entorno, y dado que se trata de un censo, esta información puede arrojar pistas sobre la población en general; perder esta diversidad nos priva de elementos relevantes en la construcción de historias a través de la ciencia de datos. Estudiar las variaciones de nombres por área geográfica, por ejemplo, puede arrojar luz sobre el contexto geo-social de la población (población inimgrante, población nativa, etc.), ya que es común que la ortografía de un nombre esté relacionada con el contexto en el que se conoció ese nombre: por ejemplo, en México, es común ver el nombre Brayan escrito de esta manera como tropicalización del nombre Brian, sin embargo, una familia de origen estadounidense llamaría Brian a su hijo, naturalmente.

b. ¿Cuántos registros hay que tengan todas las combinaciones de katelyn?

grep -iEc ',Kateleen,|,Katilynn,|,Katelyn,|,Katelynn,|,Katelin,|,Katelynne,|,Katelyne,|,Katelinn,|,Katelyn,' census_names.csv

260

Si agregamos 'Katelynd', entonces tenemos:

grep -iEc ',Kateleen,|,Katilynn,|,Katelyn,|,Katelynn,|,Katelin,|,Katelynne,|,Katelyne,|,Katelinn,|,Katelyn,' census_names.csv

280

Este será el número que usaremos (280) para verificar en el inciso d. ya que modificamos también las variaciones de 'Katelynd'

c. Modifica los registros que tengan el nombre de katelyn con todas su variantes por el que aparezca más veces (imputación), es decir, si Katelyn aparece más veces que todas las demás combinaciones, modifica todas las combinaciones a la mayor. -> Respeta la mayúscula inicial.

grep -c ',Kateleen,' census_names.csv

17

grep -c ',Katilynn,' census_names.csv

26

grep -c ',Katelyn,' census_names.csv

63

grep -c ',Katelynn,' census_names.csv

38

grep -c ',Katelin,' census_names.csv

38

grep -c ',Katelynne,' census_names.csv

31

grep -c ',Katelyne,' census_names.csv

27

grep -c ',Katelinn,' census_names.csv

20

Al final me di cuenta con grep 'Katelyn' census_names.csv que también existe 'Katelynd', por lo tanto lo metí como una variación más
grep -c ',Katelynd,' census_names.csv

20

Modificamos entonces por 'Katelyn', ya que aparece 63 veces

sed -i -E 's/,Kateleen,|,Katilynn,|,Katelyn,|,Katelynn,|,Katelin,|,Katelynne,|,Katelyne,|,Katelinn,|,Katelyn,|,Katelynd,/,Katelyn,/g' census_names.csv

d. Verifica que tienes el mismo número de registros una vez que hiciste la modificación.

grep -c 'Katelyn' census_names.csv

280
~~~

~~~
8. Jennie o Jenni o Jeni o Yenni o Yeni o Yennie
a. ¿Cuántos registros hay que tengan todas las combinaciones de Jennie?

grep -iEc ',Jennie,|,Jenni,|,Jeni,|,Yenni,|,Yeni,|,Yennie,' census_names.csv

383

b. Modifica los registros que tengan el nombre de Jennie con todas su variantes por el que aparezca más veces (imputación), es decir, si Jeni aparece más veces que todas las demás combinaciones, modifica todas las combinaciones a la mayor. -> Respeta la mayúscula inicial.

grep -ciE ',Jennie,' census_names.csv

195

grep -ciE ',Jenni,' census_names.csv

70

grep -ciE ',Jeni,' census_names.csv

69

grep -ciE ',Yenni,' census_names.csv

11

grep -ciE ',Yeni,' census_names.csv

37

grep -ciE ',Yennie,' census_names.csv

1

Modificamos entonces por 'Jennie' ya que aparece 195 veces

sed -i -E 's/,Jennie,|,Jenni,|,Jeni,|,Yenni,|,Yeni,|,Yennie,/,Jennie,/g' census_names.csv

c. Verifica que tienes el mismo número de registros una vez que hiciste la modificación.

grep -c ',Jennie,' census_names.csv

383
~~~

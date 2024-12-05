## Paso a paso Actividad 3

1. Crea un entorno virtual con la siguiente línea de comandos, ubicandote en la ruta de la carpeta del proyecto (...scrap_bets/):

    python -m venv venv1
    
2. Activa el entorno virtual, estando en la misma ruta, con el comando:

    venv1\Scripts\activate

3. Instala los paquetes necesarios estando en la ruta anterior con el comando, el proceso tarda unos segundos:

    pip install psycopg2-binary pandas openpyxl sqlalchemy selenium webdriver-manager

4. Actualiza el pip de python para evitar mostrar la alerta amarilla que aparecíó antes:

    python.exe -m pip install --upgrade pip

5. Verifica que el archivo ejecutable de Chrome Driver utilizado en clase(chromedriver.exe) se encuentre en la ruta:

    ...\scrap_bets\src\stage3\static\driver\chromedriver.exe

6. Ejecuta el archivo principal del proyecto (asegurate de que el archivo de Excel que tiene el listado general de equipos no esté abierto):

    .../scrap_bets/src/stage3/main.py

7. Verifica logs de consola, scrapeo y la creación de tablas con registros en la base de datos PostgreSQL.

8. Realiza la ejecución del archivo Power BI y confirma la conexión a la tabla tb_report para ver el reporte actualizado.
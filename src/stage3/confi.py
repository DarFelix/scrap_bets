import pkg_resources
from datetime import datetime

#variables conexión a base de datos
host="localhost"
port="5432"
nombredb="postgres"
user="postgres"
password="1234"
schema="bets"
#variables para rutas de archivos
route = pkg_resources.resource_filename(__name__,'static')#se obtiene ruta del directorio actual
route_xlsx ="{}/xlsx/names_teams.xlsx".format(route)
route_sql_rels = "{}/sql/script_relations.sql".format(route)
route_driver = "{}/driver/chromedriver.exe".format(route)
url_tyc = "https://www.tycsports.com/estadisticas/primera-division-colombia.html"
date_today = datetime.now().strftime("%Y_%m_%d")
route_screens="{}/auditoria/img/{}.png".format(route,str(date_today))
route_txt="{}/auditoria/logs/{}.txt".format(route,str(date_today))
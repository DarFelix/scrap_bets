import confi
from model import Modelo
from scrapper import Scrapper
import treat_data

#1-se crea instancia de conexión a la base de datos
model_db = Modelo(confi.host,confi.port, confi.nombredb,confi.user,confi.password)
print("------------------------")
#2-se crea esquema en base de datos
model_db.create_schema(confi.schema)
print("------------------------")
#3-se crea instancia de la clase Scrapper
scrapper = Scrapper(url=confi.url_tyc)
print("------------------------")
#4-se inicia carga página
scrapper.load_url(name_url="TyC Sports")
print("------------------------")
#5-se espera un momento que cargue correctamente
scrapper.count_load()
print("------------------------")
#6-se extrae tabla posiciones de la página en un dataframe mediante el scrapper
df_positions_teams = scrapper.get_table("posiciones")
print("------------------------")
#7-se extrae tabla goleadores de la página en un dataframe mediante el scrapper
df_scorers = scrapper.get_table("goleadores")
print("------------------------")
#8-se verifica si existe tabla paramétrica para listado de equipos (no se extrajo de una web sino de un archivo Excel, dado
#  que los equipos que están en la seria A pueden cambiar en cada torneo, porque puede bajar uno de la A y subir uno de la serie B)
exist_tb_teams = model_db.exist_table_teams("tb_teams")
print("------------------------")
#9-se obtiene diccionario de dataframes
dict_dfs = treat_data.create_dict_dfs(exist_tb_teams, df_positions_teams, df_scorers)
print("------------------------")
#10-se crea diccionario de querys de creación de tabla para cada dataframe
dict_qrs_tables = treat_data.get_querys_create_tables_dfs(dict_dfs, confi.schema)
print("------------------------")
#11-se ejecuta creación de tablas en la base de datos si no existen
model_db.create_tables(dict_qrs_tables, exist_tb_teams, True)
print("------------------------")
#12-se inserta información de los dataframes en cada tabla de la base de datos
model_db.insert_tables(dict_dfs)
print("------------------------")
#13-se captura imagen de la tabla
scrapper.screenshot_tb(xpath_tabla="//table")
#14-se auditan tablas de base de datos
model_db.audit_gen()
#15-se cierra driver
scrapper.close_driver()
#------Creación de tabla para reporte en Power BI---------------------------------
#16-se crea dataframe para reportería transformando y enriquenciendo la info disponible en base de datos
dict_report = model_db.get_dict_rp()
print("------------------------")
#17-se crea diccionario de query para crear tabla de dataframe
dict_qr_create_tb_report = treat_data.get_querys_create_tables_dfs(dict_report, confi.schema)
print("------------------------")
#18-se ejecuta creación de tabla de reporte BI en la base de datos
model_db.create_tables(dict_qr_create_tb_report)
print("------------------------")
#19-se inserta información en tabla tb_report de la base de datos
model_db.insert_tables(dict_report, mode_insert='replace')

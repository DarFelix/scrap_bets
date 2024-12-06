import pandas as pd
from io import StringIO

def create_dict_dfs(df_positions, df_scorers, exist_teams=False):
    dict_dfs = {}
    #df_teams = reader_excel.read_file()
    json_data = '[{"id_team":1,"name_team":"\u00c1guilas Doradas Rionegro","date_creation":1733429876,"date_update":1733429876},{"id_team":2,"name_team":"Alianza FC","date_creation":1733429876,"date_update":1733429876},{"id_team":3,"name_team":"Am\u00e9rica de Cali","date_creation":1733429876,"date_update":1733429876},{"id_team":4,"name_team":"At. Nacional","date_creation":1733429876,"date_update":1733429876},{"id_team":5,"name_team":"Atl\u00e9tico F. C.","date_creation":1733429876,"date_update":1733429876},{"id_team":6,"name_team":"Atl\u00e9tico Huila","date_creation":1733429876,"date_update":1733429876},{"id_team":7,"name_team":"Barranquilla F. C.","date_creation":1733429876,"date_update":1733429876},{"id_team":8,"name_team":"Boca Juniors de Cali","date_creation":1733429876,"date_update":1733429876},{"id_team":9,"name_team":"Bogot\u00e1 F. C.","date_creation":1733429876,"date_update":1733429876},{"id_team":10,"name_team":"Boyac\u00e1 Chic\u00f3","date_creation":1733429876,"date_update":1733429876},{"id_team":11,"name_team":"Bucaramanga","date_creation":1733429876,"date_update":1733429876},{"id_team":12,"name_team":"C\u00facuta Deportivo","date_creation":1733429876,"date_update":1733429876},{"id_team":13,"name_team":"Deportes Quind\u00edo","date_creation":1733429876,"date_update":1733429876},{"id_team":14,"name_team":"Deportivo Cali","date_creation":1733429876,"date_update":1733429876},{"id_team":15,"name_team":"Envigado","date_creation":1733429876,"date_update":1733429876},{"id_team":16,"name_team":"Fortaleza FC","date_creation":1733429876,"date_update":1733429876},{"id_team":17,"name_team":"Independiente Medell\u00edn","date_creation":1733429876,"date_update":1733429876},{"id_team":18,"name_team":"Internacional F. C. de Palmira","date_creation":1733429876,"date_update":1733429876},{"id_team":19,"name_team":"Itag\u00fc\u00ed Leones","date_creation":1733429876,"date_update":1733429876},{"id_team":20,"name_team":"Jaguares","date_creation":1733429876,"date_update":1733429876},{"id_team":21,"name_team":"Junior","date_creation":1733429876,"date_update":1733429876},{"id_team":22,"name_team":"La Equidad","date_creation":1733429876,"date_update":1733429876},{"id_team":23,"name_team":"Llaneros","date_creation":1733429876,"date_update":1733429876},{"id_team":24,"name_team":"Millonarios","date_creation":1733429876,"date_update":1733429876},{"id_team":25,"name_team":"Once Caldas","date_creation":1733429876,"date_update":1733429876},{"id_team":26,"name_team":"Orsomarso S. C.","date_creation":1733429876,"date_update":1733429876},{"id_team":27,"name_team":"Pasto","date_creation":1733429876,"date_update":1733429876},{"id_team":28,"name_team":"Patriotas FC","date_creation":1733429876,"date_update":1733429876},{"id_team":29,"name_team":"Pereira","date_creation":1733429876,"date_update":1733429876},{"id_team":30,"name_team":"Real Cartagena","date_creation":1733429876,"date_update":1733429876},{"id_team":31,"name_team":"Real Cundinamarca","date_creation":1733429876,"date_update":1733429876},{"id_team":32,"name_team":"Real Santander","date_creation":1733429876,"date_update":1733429876},{"id_team":33,"name_team":"Santa Fe","date_creation":1733429876,"date_update":1733429876},{"id_team":34,"name_team":"Tigres F. C.","date_creation":1733429876,"date_update":1733429876},{"id_team":35,"name_team":"Tolima","date_creation":1733429876,"date_update":1733429876},{"id_team":36,"name_team":"Uni\u00f3n Magdalena","date_creation":1733429876,"date_update":1733429876}]'
    df_teams = pd.read_json(StringIO(json_data))
    df_positions["date_creation"] = pd.to_datetime(pd.Timestamp.now())
    df_positions["update_creation"] = pd.to_datetime(pd.Timestamp.now())
    df_scorers["date_creation"] = pd.to_datetime(pd.Timestamp.now())
    df_scorers["update_creation"] = pd.to_datetime(pd.Timestamp.now())

    map_ids = dict(zip(df_teams["name_team"], df_teams["id_team"]))
    df_positions["id_team"] = df_positions["name_team"].map(map_ids)
    df_positions = df_positions.rename(columns={"Pos": "value_position", "Pts": "current_points", "Pj": "played_games", "Pg": "win_games","Pe": "draw_games", "Pp": "lost_games", "Gf": "goals_for", "Gc": "goals_against"})
    df_positions = df_positions[["id_team", "value_position","current_points","played_games","win_games","draw_games","lost_games","goals_for","goals_against","date_creation","update_creation"]]

    df_scorers["id_team"] = df_scorers["name_team"].map(map_ids)
    df_scorers = df_scorers.rename(columns={"Jugador": "name_player", "Goles": "current_goals"})
    df_scorers = df_scorers[["name_player", "id_team","current_goals","date_creation","update_creation"]]


    if not exist_teams:
        dict_dfs["tb_teams"]=df_teams
        dict_dfs["tb_positions"]=df_positions
        dict_dfs["tb_scorers"]=df_scorers
        return dict_dfs;
    else:
        dict_dfs["tb_positions"]=df_positions
        dict_dfs["tb_scorers"]=df_scorers
        return dict_dfs;

# se crea función para generar query que permita crear una tabla en base de datos sin registros
# a partir de la estructura de un dataframe, de manera dinámica
def get_querys_create_tables_dfs(dict_dfs, name_schema):
    #diccionario vacío que se llenara con las querys para cada tabla
    dict_qrs = {}
    # se agregan nombres de hojas de Excel que serán los nombres de tablas en una lista
    name_tables = list(dict_dfs.keys())
    #se recorre cada dataframe para extraer la consulta SQL que permitira crear la tabla en base de datos
    for name_tb in name_tables:
        #se extrae cada dataframe
        df = dict_dfs[name_tb]
        #se crea query inicial de creación de tabla por cada df
        str_qr = 'CREATE TABLE IF NOT EXISTS '+name_schema+'.'+name_tb+' (id SERIAL NOT NULL,'
        idx = 0
        #se recorre cada columna para determinar su tipo de dato
        for col in df.columns:
            #según el tipo de dato se asigna el valor correspondiente
            atr_row = ''
            if(df[col].dtype == 'int64') or (df[col].dtype == 'int32'):
                atr_row = 'INT NOT NULL'
            elif(df[col].dtype == 'float64') or (df[col].dtype == 'float32'):
                atr_row = 'REAL NOT NULL'
            elif(df[col].dtype == 'datetime64[ns]' or df[col].dtype == 'datetime64[us]'):
                atr_row = 'TIMESTAMP'
            elif(df[col].dtype == 'object'):
                atr_row = 'VARCHAR(50) NOT NULL'
            idx+=1
            str_qr+=col+' '+atr_row+','
        str_qr = str_qr[:-1] + ")"
        idx = 0
        dict_qrs[name_tb]=str_qr
    print("Creación de diccionario de querys para crear tablas")
    return dict_qrs
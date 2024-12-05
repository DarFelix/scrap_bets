import reader_excel
import pandas as pd

def create_dict_dfs(exist_teams, df_positions, df_scorers):
    dict_dfs = {}
    df_teams = reader_excel.read_file()
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
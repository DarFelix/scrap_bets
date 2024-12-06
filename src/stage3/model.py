from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import confi
import pandas as pd
from io import StringIO

class Modelo:
    def __init__(self, host="", port="", nombredb="", user="", password="",schema=""):
        self.host = host
        self.port = port
        self.nombredb = nombredb
        self.user = user
        self.password = password
        self.schema = schema
        self.conection = None
        #self.conect()
    """ 
    def conect(self):
        try:
            self.conection = create_engine(
                f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.nombredb}', echo=False
            )
            with self.conection.connect():
                print("Conexión exitosa")
        except SQLAlchemyError as e:
            print(f"Conexión errónea: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la conexión: {e}")
    
    def create_schema(self, nombre_schema=""):
        try:
            with self.conection.connect() as conexion:
                create_schema = f'CREATE SCHEMA IF NOT EXISTS {nombre_schema};'
                conexion = conexion.execution_options(isolation_level="AUTOCOMMIT")
                conexion.execute(text(create_schema))
                print("Creación de esquema exitosa")
        except SQLAlchemyError as e:
            print(f"Error al crear el esquema: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al crear el esquema: {e}")

    def run_querys_dict(self, dict_querys = None):
        try: 
            name_tables = list(dict_querys.keys())
            for table in name_tables:
                with self.conection.connect() as conexion:
                    conexion = conexion.execution_options(isolation_level="AUTOCOMMIT")
                    conexion.execute(text(dict_querys[table]))
                    print("Creación exitosa de tabla: "+table)
        except SQLAlchemyError as e:
            print(f"Creación errónea de tabla: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al crear la tabla: {e}")
    
    def create_tables(self, dict_querys=None, exist_tb_teams=False, are_main_tbs = False):
        if not exist_tb_teams and dict_querys and are_main_tbs:
            self.run_querys_dict(dict_querys)
            self.create_relations(confi.route_sql_rels)
        else:
            self.run_querys_dict(dict_querys)
    
    def insert_tables(self, dict_dfs, mode_insert='append'):
        try:
            name_tables = list(dict_dfs.keys())
            for name_tb in name_tables:
                with self.conection.connect() as conexion:
                    dict_dfs[name_tb].to_sql(name_tb, con=conexion, schema=confi.schema, if_exists=mode_insert, index=False)
                    print(f"Se insertó correctamente en {name_tb}")
        except SQLAlchemyError as e:
            print(f"No se insertó en {name_tb}, error: {e}")
        except TypeError as e:
            print(f"Error de tipo al insertar en {name_tb}: {e}")
        except Exception as e:
            print(f"No se insertó en {name_tb}, error inesperado: {e}")


    def create_relations(self, route_sql_relations=""):
        try:
            with open(route_sql_relations, 'r') as file:
                script_relations = file.read()
            with self.conection.connect() as conexion:
                conexion = conexion.execution_options(isolation_level="AUTOCOMMIT")
                conexion.execute(text(script_relations))
                print("Creación exitosa de relaciones")
        except FileNotFoundError as e:
            print(f"Archivo SQL no encontrado: {e}")
        except SQLAlchemyError as e:
            print(f"Creación errónea de relaciones: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al crear las relaciones: {e}")

    def exist_table_teams(self, name_tb=""):
        try:
            df = pd.read_sql(f"SELECT * FROM "+confi.schema+"."+name_tb, con=self.conection)
            if not df.empty:
                return True
        except Exception:
            return False;

    def audit_tb(self, name_tb):
        try:
        
            df = pd.read_sql(f"SELECT * FROM {confi.schema}.{name_tb}", con=self.conection)
            with open(confi.route_txt+"_"+name_tb, 'w') as archivo:
                archivo.write("Información del DataFrame:\n")
                buffer = StringIO()
                df.info(buf=buffer)
                archivo.write(buffer.getvalue() + "\n\n")
                archivo.write("Estadísticas descriptivas:\n")
                archivo.write(df.describe().to_string() + "\n\n")
                archivo.write("Número de valores nulos por columna:\n")
                archivo.write(df.isnull().sum().to_string() + "\n\n")
                archivo.write("Dimensiones del DataFrame:\n")
                archivo.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}\n")

            print(f"Auditoría de la tabla '{name_tb}' guardada en: {confi.route_txt}_{name_tb}")

        except SQLAlchemyError as e:
            print(f"Error al consultar la tabla '{name_tb}': {e}")
        except Exception as e:
            print(f"Error al auditar la tabla '{name_tb}': {e}")

    def audit_gen(self):
        self.audit_tb("tb_teams")
        print("----------")
        self.audit_tb("tb_positions")
        print("----------")
        self.audit_tb("tb_scorers")
        print("----------")

    def read_one_tb(self, name_tb=""):
        try:
            df = pd.read_sql(f"SELECT * FROM "+confi.schema+"."+name_tb, con=self.conection)
            if not df.empty:
                return df
            else:
                return pd.DataFrame()
        except Exception as e:
            print("Error al leer tabla: "+str(e))
            return pd.DataFrame()
        
    

    """

    def get_dict_rp(self, dict_dfs):
        #se extraen dataframes de las tablas de bases de datos existentes
        tb_positions = dict_dfs["tb_positions"]
        tb_scorers = dict_dfs["tb_scorers"]
        tb_teams = dict_dfs["tb_teams"]
        #se arma un diccionario con los datos de las tablas extraidas
        dict_tbs = {}
        dict_tbs["tb_positions"]=tb_positions
        dict_tbs["tb_scorers"]=tb_scorers
        dict_tbs["tb_teams"]=tb_teams
        #se transforman y enriquecen datos de tablas, se crea dataframe para reporteria
        df_report = self.transform_dfs(dict_tbs)
        dict_rp = {}
        dict_rp["tb_report"] = df_report
        #se regresa diccionario con dataframe para reporteria
        print("se devuelve dataframe de reporte ya transformado")
        return dict_rp

    def transform_dfs(self, dict_tbs):
        tb_positions = dict_tbs["tb_positions"]
        tb_scorers = dict_tbs["tb_scorers"]
        tb_teams = dict_tbs["tb_teams"]
        print("se enriquece información de tablas de base de datos")
        #se cambia nombre columna 'id'
        tb_positions = tb_positions.rename(columns={'id': 'id_new'})
        #se cambia tipo de dato en algunas columnas
        tb_positions['value_position'] = tb_positions['value_position'].astype(int)
        tb_positions['current_points'] = tb_positions['current_points'].astype(int)
        tb_positions['goals_for'] = tb_positions['goals_for'].astype(int)
        tb_positions['goals_against'] = tb_positions['goals_against'].astype(int)
        tb_positions['played_games'] = tb_positions['played_games'].astype(int)
        tb_positions['win_games'] = tb_positions['win_games'].astype(int)
        tb_positions['draw_games'] = tb_positions['draw_games'].astype(int)
        tb_positions['lost_games'] = tb_positions['lost_games'].astype(int)

        #se califica un equipo como "WINNER", "DRAWER" o "LOSER", dependiendo de la mayoria de partidos
        tb_positions['calification'] = tb_positions[['win_games', 'draw_games', 'lost_games']].idxmax(axis=1)
        califications = {
            'win_games' : 'WINNER',
            'draw_games' : 'DRAWER',
            'lost_games' : 'LOSER'
        }
        tb_positions['calification'] = tb_positions['calification'].map(califications)
        #columnas calculadas
        tb_positions['year_creation'] = tb_positions['date_creation'].dt.year

        names_month = {
            1 : 'Enero',
            2 : 'Febrero',
            3 : 'Marzo',
            4 : 'Abril',
            5 : 'Mayo',
            6 : 'Junio',
            7 : 'Julio',
            8 : 'Agosto',
            9 : 'Septiembre',
            10 : 'Octubre',
            11 : 'Noviembre',
            12 : 'Diciembre'
        }

        tb_positions['month_creation'] = tb_positions['date_creation'].dt.month.map(names_month)
        tb_positions['day_creation'] = tb_positions['date_creation'].dt.day

        names_week = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }

        tb_positions['day_creation_name'] = tb_positions['date_creation'].dt.day_name().map(names_week)
        tb_positions['date_text'] = tb_positions['date_creation'].dt.strftime("%d%b%Y")
        tb_positions["dif_goals"]=tb_positions["goals_for"] - tb_positions["goals_against"]
        tb_positions["av_goals_for_game"] = round(tb_positions['goals_for'] / tb_positions['played_games'], 2)
        #calculos tabla de goleadores
        tb_scorers['current_goals'] = tb_scorers['current_goals'].astype(int)
        tb_scorers['total_goals_scorers_team'] = tb_scorers.groupby(['id_team','date_creation'])['current_goals'].transform('sum')
        tb_scorers['total_scorers_team'] = tb_scorers.groupby(['id_team','date_creation'])['id_team'].transform('size')
        date_max_scorers = tb_scorers['date_creation'].max()
        # se filtran los registros mas recientes de goleadores
        filt_scorers = tb_scorers.loc[tb_scorers['date_creation'] == date_max_scorers]
        filt_scorers = filt_scorers.drop_duplicates(subset=['id_team'], keep='first')
        filt_scorers = filt_scorers[['id_team', 'total_goals_scorers_team', 'total_scorers_team']]
        #se unen dataframes, conservando las columnas de interes
        df_merge = pd.merge(tb_positions, filt_scorers, on='id_team', how='left')
        df_merge["advan_pts_team_before"]= tb_positions['current_points'] - tb_positions['current_points'].shift(-1)
        #se calcula column goles a favor en fecha anterior y diferencia de goles respecto a la fecha anterior
        df_merge = df_merge.sort_values(by=['id_team', 'date_creation'])
        df_merge['goals_for_before_date'] = df_merge.groupby('id_team')['goals_for'].shift(1)
        df_merge["dif_goals_for"] = df_merge["goals_for"] - df_merge['goals_for_before_date']
        #se agrega nombre del equipo
        df_merge = pd.merge(df_merge, tb_teams[["id_team", "name_team"]], on='id_team', how='left')
        #se filtran registros recientes
        date_max_rp = df_merge['date_creation'].max()
        df_merge = df_merge.loc[df_merge['date_creation'] == date_max_rp]
        #se ordenan registros en orden ascendente por la posición
        df_report = df_merge.sort_values(by='value_position', ascending=True)
        #se cambian nulos por cero
        df_report = df_report.fillna(0)
        print(df_report.info())
        #se regresa dataframe para ser utilizado en reportería
        return df_report


import pandas as pd
import confi

# se crea función para leer contenido de excel
def read_file():
    try:
        # se devuelve un dataframe con el listado de equipos
        sheets_dict = pd.read_excel(confi.route_xlsx, sheet_name=None);
        print("Lectura correcta de listado de equipos")
        df_teams = sheets_dict['tb_teams']
        df_teams["date_creation"] = pd.to_datetime(pd.Timestamp.now())
        df_teams["date_update"] = pd.to_datetime(pd.Timestamp.now())
        return df_teams;
    except Exception as e:
        print("Error al leer listado de equipos"+e)
        return
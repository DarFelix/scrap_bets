import pandas as pd # genera informacion matricial 
import time
from selenium import webdriver # importa el modulo de webdriver
from selenium.webdriver.common.by import By #localiza elemento en una pagina web
from selenium.webdriver.chrome.service import Service as ChromeService # Clase servicio para levantar driver chrome
import pandas as pd
import confi
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scrapper:
    def __init__(self, url=""):
        self.url=url
        options = webdriver.ChromeOptions() #permite configurar el navegador
        options.add_argument('--no-sandbox') 
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")
        if len(confi.route_driver) >0:
            self.service = ChromeService(executable_path= confi.route_driver)
            self.driver = webdriver.Chrome(service=self.service, options=options)
            self.driver.maximize_window()
        else:
            self.driver = webdriver.Chrome(options=options)

    def load_url(self, name_url=""):
        self.driver.get(self.url)
        print("************Se carga url:"+name_url+"**************")

    def get_table(self,id_table=""):
        try:
            tb_element = self.driver.find_element(By.ID, id_table)
            if tb_element:
                tb_headers = [th.text for th in tb_element.find_elements(By.TAG_NAME, 'th')]
                if tb_headers[1] == '':
                    tb_headers[1] = 'name_team'
                # Extraer filas de la tabla
                rows = tb_element.find_elements(By.TAG_NAME, 'tr')
                data_df = []
                for rw in rows[1:]:  # Saltar la primera fila si contiene encabezados
                    cells = rw.find_elements(By.TAG_NAME, 'td')
                    cell_texts = []
                    for cell in cells:
                        cell_texts.append(cell.text)
                        try:
                            # Busca un elemento <img> dentro del contenedor
                            imagen = cell.find_element(By.TAG_NAME, "img")
                            # Si se encuentra se obtiene atributo "alt" que contiene el nombre del equipo
                            cell_texts.append(imagen.get_attribute("alt"))
                        except:
                            pass
                    del cell_texts[1]
                    data_df.append(cell_texts)

            df_formed = pd.DataFrame(data_df, columns=tb_headers)
            print("Scrapeo correcto tabla con id: "+id_table)
            return df_formed
        except print(0):
            pass

    def count_load(self):
        print("Espera por favor...")
        count = 0
        while count < 10:
            count+=1
            time.sleep(1)
            print(str(count)+"/10 segundos")
        print("Falta poco...")
    
    def screenshot_tb(self, xpath_tabla):
        #Captura una imagen de la tabla identificada por un xpath específico y la guarda en una ruta.
        try:
            tabla_element = self.driver.find_element(By.XPATH, xpath_tabla)
            if tabla_element:
                tabla_element.screenshot(confi.route_screens)
                print(f"Imagen de la tabla capturada y guardada en: {confi.route_screens}")
        except Exception as e:
            print(f"Error al capturar la imagen de la tabla: {e}")

    def close_driver(self):
        self.driver.quit()

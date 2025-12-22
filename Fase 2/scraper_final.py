from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd # Importamos Pandas para guardar los datos
import time
import random

# --- CONFIGURACIÓN ---
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
opts.add_argument("--headless") # Descomenta esto en producción para no ver el navegador

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# URL Base: Fíjate que dejamos el espacio {} para poner el número de paginación
url_base = "https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana/_Desde_{}_NoIndex_True"

datos_totales = [] # Aquí guardaremos cada casa como un diccionario

# --- BUCLE DE PÁGINAS (Scrapeamos 3 páginas: 1, 49, 97) ---
for i in range(1, 145, 48): 
    
    url_actual = url_base.format(i)
    print(f"Scrapeando página: {url_actual}")
    
    driver.get(url_actual)
    time.sleep(random.uniform(3, 5)) # Espera humana para evitar bloqueos
    
    # 1. Encontrar el CONTENEDOR de cada aviso
    # Usamos una clase muy común en ML/Portal. Si falla, avísame.
    cards = driver.find_elements(By.CLASS_NAME, "ui-search-layout__item")
    
    print(f"-> Encontré {len(cards)} avisos en esta página.")

    # 2. Iterar sobre cada tarjeta encontrada
    for card in cards:
        try:
            # Extracción segura: Si falla un dato, no rompe el script
            
            # PRECIO (Tu clase)
            try:
                precio = card.find_element(By.CLASS_NAME, "poly-price__current").text
            except:
                precio = "N/A"

            # UBICACIÓN (Tu clase)
            try:
                ubicacion = card.find_element(By.CLASS_NAME, "poly-component__location").text
            except:
                ubicacion = "N/A"

            # ATRIBUTOS (Tu clase)
            try:
                # Esto trae todo el texto junto (ej: "50 m² 2 dorms")
                # Luego lo limpiaremos con Python
                attrs = card.find_element(By.CLASS_NAME, "poly-component__attributes-list").text
            except:
                attrs = "N/A"
            
            # Guardamos en un diccionario
            datos_totales.append({
                "Precio": precio,
                "Ubicacion": ubicacion,
                "Detalles": attrs
            })
            
        except Exception as e:
            print(f"Error en una tarjeta: {e}")

# --- CIERRE Y GUARDADO ---
driver.quit()

print(f"Total de propiedades extraídas: {len(datos_totales)}")

# Convertir a DataFrame de Pandas
df = pd.DataFrame(datos_totales)

# Limpieza rápida (quitar saltos de línea molestos)
df = df.replace(r'\n',' ', regex=True) 

# Guardar a CSV
nombre_archivo = "resultados_inmobiliarios.csv"
df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig') # utf-8-sig para que Excel lea bien las ñ y tildes

print(f"¡Éxito! Datos guardados en {nombre_archivo}")
print(df.head()) # Muestra las primeras 5 filas
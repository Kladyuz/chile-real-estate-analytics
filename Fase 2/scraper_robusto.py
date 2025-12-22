from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random

# --- CONFIGURACIÓN ---
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
# opts.add_argument("--headless") 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

url_base = "https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana/_Desde_{}_NoIndex_True"
datos_totales = []

# --- FUNCIONES DE AYUDA (Para probar múltiples clases) ---
def buscar_texto(elemento, selectores):
    """Prueba una lista de selectores CSS y devuelve el texto del primero que encuentre."""
    for selector in selectores:
        try:
            encontrado = elemento.find_element(By.CSS_SELECTOR, selector).text
            if encontrado:
                return encontrado
        except:
            continue # Si falla, prueba el siguiente
    return None # Si fallan todos

# --- BUCLE DE PÁGINAS ---
# Vamos a probar con 2 páginas (96 registros) para verificar primero
for i in range(1, 97, 48): 
    
    url_actual = url_base.format(i)
    print(f"--- Scrapeando página: {url_actual} ---")
    driver.get(url_actual)
    
    # Scroll lento hasta el final para forzar la carga de imágenes/datos (Lazy Loading)
    print("Haciendo scroll para cargar elementos...")
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)
    
    time.sleep(random.uniform(2, 4))
    
    # Buscamos las tarjetas (El contenedor también puede variar)
    cards = driver.find_elements(By.CSS_SELECTOR, "li.ui-search-layout__item")
    
    print(f"-> Encontré {len(cards)} tarjetas.")

    for card in cards:
        item = {}
        
        # 1. PRECIO: Probamos clase nueva (poly) y vieja (ui-search) y genérica
        selectores_precio = [
            '.poly-price__current', 
            '.ui-search-price__part', 
            '.price-tag-text-sr-only',
            '.andes-money-amount__fraction' # A veces el precio es solo el número
        ]
        item['Precio'] = buscar_texto(card, selectores_precio)

        # 2. UBICACIÓN
        selectores_ubicacion = [
            '.poly-component__location', 
            '.ui-search-item__location',
            '.ui-search-item__group__element.ui-search-item__location'
        ]
        item['Ubicacion'] = buscar_texto(card, selectores_ubicacion)

        # 3. DETALLES (M2, Dorms)
        selectores_detalles = [
            '.poly-component__attributes-list', 
            '.ui-search-card-attributes',
            '.ui-search-item__group__element.ui-search-item__attributes'
        ]
        item['Detalles'] = buscar_texto(card, selectores_detalles)

        # 4. FAIL-SAFE: Si todo falla, guardamos el texto crudo para analizar después
        if item['Precio'] is None:
            item['Raw_Data'] = card.text # Guarda todo el texto sucio de la tarjeta
        else:
            item['Raw_Data'] = "OK"

        datos_totales.append(item)

driver.quit()

# --- GUARDADO ---
df = pd.DataFrame(datos_totales)
df = df.replace(r'\n',' ', regex=True)

# Revisión Rápida
print(f"\nResumen de Extracción:")
print(f"Total registros: {len(df)}")
print(f"Registros con Precio capturado: {df['Precio'].notnull().sum()}")
print(df.head())

df.to_csv("resultados_inmobiliarios_v2.csv", index=False, encoding='utf-8-sig')
print("Archivo guardado: resultados_inmobiliarios_v2.csv")
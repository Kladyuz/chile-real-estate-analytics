from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup # Importamos BS4 para parsear
import pandas as pd
import time
import random

# --- CONFIGURACIÓN ---
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
# opts.add_argument("--headless") # Puedes descomentar esto para que no abra la ventana

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

url_base = "https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana/_Desde_{}_NoIndex_True"
datos_totales = []

# --- BUCLE DE PÁGINAS ---
# Probemos con 3 páginas (aprox 150 resultados)
for i in range(1, 145, 48): 
    
    url_actual = url_base.format(i)
    print(f"--- Procesando página: {i} (URL: {url_actual}) ---")
    driver.get(url_actual)
    
    # Scroll humano para asegurar carga de imágenes y datos lazy-loaded
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1)
    
    time.sleep(2) # Espera final
    
    # --- AQUÍ ESTÁ LA MAGIA ---
    # En lugar de pedirle a Selenium que busque elemento por elemento,
    # le pedimos todo el código HTML de una sola vez y se lo damos a BeautifulSoup.
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Buscamos las tarjetas en el HTML estático (es mucho más rápido)
    cards = soup.find_all('li', class_='ui-search-layout__item')
    print(f"-> Tarjetas detectadas por BS4: {len(cards)}")

    for card in cards:
        try:
            # 1. PRECIO
            # Buscamos la clase poly que confirmaste que existe
            precio_tag = card.find('span', class_='poly-price__current') or card.find('div', class_='poly-price__current')
            precio = precio_tag.get_text(strip=True) if precio_tag else None

            # 2. UBICACIÓN
            ubicacion_tag = card.find('span', class_='poly-component__location') or card.find('div', class_='poly-component__location')
            ubicacion = ubicacion_tag.get_text(strip=True) if ubicacion_tag else None

            # 3. DETALLES (M2 y Dorms)
            # A veces es una lista, a veces un span. Buscamos genérico.
            detalles_tag = card.find('ul', class_='poly-component__attributes-list') or card.find('div', class_='poly-component__attributes-list')
            if detalles_tag:
                # Extraemos todo el texto y quitamos espacios extra
                detalles = " ".join(detalles_tag.get_text(separator=" ").split())
            else:
                detalles = None

            # Solo guardamos si al menos tenemos precio (para no guardar basura)
            if precio:
                datos_totales.append({
                    "Precio": precio,
                    "Ubicacion": ubicacion,
                    "Detalles": detalles
                })
                
        except Exception as e:
            print(f"Error parseando una tarjeta: {e}")

driver.quit()

# --- GUARDADO Y RESULTADOS ---
df = pd.DataFrame(datos_totales)

print(f"\n========================================")
print(f"RESUMEN FINAL")
print(f"Total propiedades capturadas: {len(df)}")
print(f"========================================")

if not df.empty:
    print(df.head(10))
    # Limpieza básica: separar el símbolo de moneda si viene pegado (opcional)
    # Guardamos
    df.to_csv("dataset_inmobiliario_final.csv", index=False, encoding='utf-8-sig')
    print("Archivo guardado: dataset_inmobiliario_final.csv")
else:
    print("Algo salió mal. El DataFrame está vacío.")
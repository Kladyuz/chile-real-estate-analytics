from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración básica
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

print("--- INICIANDO MODO DEBUG ---")
driver.get("https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana")
time.sleep(5)

# Buscamos las tarjetas
cards = driver.find_elements(By.CSS_SELECTOR, "li.ui-search-layout__item")
print(f"Tarjetas encontradas: {len(cards)}")

found_failed_card = False

for i, card in enumerate(cards):
    try:
        # Intentamos ver si tiene la clase "poly" (la que sí funcionó antes)
        # Si NO la tiene, es una de las que nos falla. Queremos ver ESA.
        try:
            card.find_element(By.CLASS_NAME, "poly-price__current")
            es_poly = True
        except:
            es_poly = False
        
        if not es_poly:
            print(f"\n!!! ENCONTRÉ UNA TARJETA QUE FALLA (Índice {i}) !!!")
            print("Copiando su estructura interna...")
            print("="*50)
            
            # ESTO ES LO QUE NECESITO: El HTML interno de la tarjeta
            html_content = card.get_attribute('innerHTML')
            print(html_content) 
            
            print("="*50)
            found_failed_card = True
            break # Solo necesitamos una para analizar
            
    except Exception as e:
        print(e)

if not found_failed_card:
    print("Curioso... todas parecen tener la clase poly. ¿Seguro que fallaron?")

driver.quit()
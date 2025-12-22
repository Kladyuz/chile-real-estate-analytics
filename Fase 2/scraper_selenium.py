from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# 1. Configuración del Navegador
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# opts.add_argument("--headless") # <- Si quitas el comentario (#), el navegador no se verá (se ejecuta en fondo)

print("Iniciando navegador...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# 2. Navegar a la URL
url = "https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana"
driver.get(url)

# 3. Esperar a que cargue (Wait)
# Aquí esperamos 5 segundos para asegurar que el JavaScript traiga los precios
print("Esperando renderizado...")
time.sleep(5) 

# 4. Extracción
try:
    # Usamos las clases que TÚ encontraste: 'poly-price__current'
    # El punto . al inicio significa "clase" en selector CSS
    precios = driver.find_elements(By.CSS_SELECTOR, ".poly-price__current")
    
    # Intentamos buscar los títulos también para tener contexto
    titulos = driver.find_elements(By.CSS_SELECTOR, ".poly-component__title") # A veces cambia, probemos esta

    print(f"----------------------------------------")
    print(f"Resultados encontrados: {len(precios)}")
    print(f"----------------------------------------")

    if len(precios) > 0:
        for i in range(min(5, len(precios))): # Imprimir solo los primeros 5
            texto_precio = precios[i].text
            print(f"Propiedad {i+1}: {texto_precio}")
    else:
        print("Aún no los encontramos. Puede que la clase haya cambiado o el selector sea incorrecto.")

except Exception as e:
    print(f"Ocurrió un error: {e}")

# 5. Cerrar
print("Cerrando navegador...")
driver.quit()
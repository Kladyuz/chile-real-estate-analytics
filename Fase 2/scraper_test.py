import requests
from bs4 import BeautifulSoup
import time
import random

# 1. Configuración
url = "https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

print(f"Scrapeando: {url}")

# 2. Petición
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Conexión exitosa (200 OK). Analizando HTML...")
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3. Búsqueda usando TUS clases encontradas
    # Buscamos todos los elementos que tengan la clase del precio actual
    precios = soup.find_all('span', class_='poly-price__current')
    
    # Intento alternativo (a veces usan div en vez de span)
    if not precios:
        precios = soup.find_all('div', class_='poly-price__current')

    print(f"----------------------------------------")
    print(f"Resultados encontrados: {len(precios)}")
    print(f"----------------------------------------")

    if len(precios) > 0:
        print("¡ÉXITO! Se puede usar BeautifulSoup (Más rápido).")
        # Imprimimos los primeros 5 para ver qué formato tienen
        for i, precio in enumerate(precios[:5]):
            print(f"{i+1}. {precio.text.strip()}")
    else:
        print("FALLO: No se encontraron precios con esa clase.")
        print("HIPÓTESIS: La página carga los datos con JavaScript dinámico.")
        print("ACCIÓN REQUERIDA: Cambiar a Selenium.")

else:
    print(f"Error de conexión: {response.status_code}")
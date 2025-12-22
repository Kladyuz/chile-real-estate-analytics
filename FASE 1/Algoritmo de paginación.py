# Lógica que usaremos en el código
base_url = "https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana/_Desde_{}_NoIndex_True"

# Generamos las URLs para las primeras 5 páginas
for i in range(1, 241, 48): # Empieza en 1, termina en 241, salta de 48 en 48
    url = base_url.format(i)
    print(url)
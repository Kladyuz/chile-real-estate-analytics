import pandas as pd
import re # Librería de Expresiones Regulares (Crucial para limpieza)

# 1. Cargar datos
df = pd.read_csv(r"C:\Users\javie\Desktop\Javier Ingeniero\Portfolio_Projects\proyecto_inmobiliario\FASE 3\dataset_inmobiliario_final.csv")

# Valor de la UF actual (puedes actualizarlo o sacarlo de una API más adelante)
VALOR_UF = 38000 

def limpiar_precio(texto_precio):
    """
    Recibe: "UF 3.372" o "$ 150.000.000"
    Devuelve: El valor entero en PESOS (CLP)
    """
    if pd.isna(texto_precio):
        return None
    
    # Convertimos a string por seguridad
    texto = str(texto_precio).strip()
    
    # Caso 1: Es UF
    if "UF" in texto:
        # Quitamos "UF", puntos y espacios. Reemplazamos coma decimal si existe.
        # Ejemplo: "UF 3.372" -> "3372"
        limpio = re.sub(r'[^\d,]', '', texto) 
        try:
            valor_uf = float(limpio.replace(',', '.'))
            return int(valor_uf * VALOR_UF)
        except:
            return None
            
    # Caso 2: Es Pesos ($)
    elif "$" in texto or len(texto) > 6: # Asumimos pesos si es un número muy grande
        # Quitamos "$", puntos y espacios
        limpio = re.sub(r'[^\d]', '', texto)
        try:
            return int(limpio)
        except:
            return None
    
    return None

# Aplicamos la función a la columna
print("Transformando precios...")
df['precio_en_pesos'] = df['Precio'].apply(limpiar_precio)

# Verificación
print("\n--- Precios Originales vs Transformados ---")
print(df[['Precio', 'precio_en_pesos']].head(10))

# Estadísticas rápidas
print("\n--- Estadísticas de Precio (CLP) ---")
print(df['precio_en_pesos'].describe().apply(lambda x: format(x, 'f')))
import pandas as pd
import re
import numpy as np

# 1. Cargar el dataset con precios ya limpios
# OJO: Asegúrate de guardar el CSV anterior con la columna nueva, 
# o usa este script asumiendo que partes del original y repites la limpieza de precios.
# Para simplificar, aquí repito la limpieza de precio rápida y agrego lo nuevo.

df = pd.read_csv(r"C:\Users\javie\Desktop\Javier Ingeniero\Portfolio_Projects\proyecto_inmobiliario\FASE 3\dataset_inmobiliario_final.csv")

# --- REPETICIÓN LIMPIEZA PRECIO (Por si acaso) ---
VALOR_UF = 38000 
def limpiar_precio(texto):
    if pd.isna(texto): return None
    texto = str(texto).strip()
    if "UF" in texto:
        limpio = re.sub(r'[^\d,]', '', texto) 
        try: return int(float(limpio.replace(',', '.')) * VALOR_UF)
        except: return None
    elif "$" in texto or len(texto) > 6:
        limpio = re.sub(r'[^\d]', '', texto)
        try: return int(limpio)
        except: return None
    return None

df['precio_peso'] = df['Precio'].apply(limpiar_precio)

# --- NUEVA LÓGICA: EXTRAER DETALLES ---

def extraer_numeros(texto, patron):
    """Busca números o rangos (ej: '23 - 38') y devuelve el promedio."""
    if pd.isna(texto): return None
    
    # Busca números asociados al patrón (ej: antes de 'm²')
    # Regex explicaicón: (\d+) busca digitos, (?:-\s*(\d+))? busca opcionalmente un guion y otro numero
    match = re.search(fr'(\d+(?:[\.,]\d+)?)\s*(?:-\s*(\d+(?:[\.,]\d+)?))?\s*{patron}', str(texto), re.IGNORECASE)
    
    if match:
        val1 = float(match.group(1).replace(',', '.'))
        if match.group(2): # Si existe un segundo número (rango)
            val2 = float(match.group(2).replace(',', '.'))
            return (val1 + val2) / 2 # Retornamos promedio
        return val1
    return None

def limpiar_dorms(texto):
    if pd.isna(texto): return None
    texto = str(texto).lower()
    
    # Caso especial: Estudio
    if 'estudio' in texto and 'dorm' not in texto:
        return 1.0 # Asumimos 1 ambiente
        
    # Buscar "X dorm"
    dorms = extraer_numeros(texto, 'dorm')
    
    # Si no encontró número pero dice "Estudio", devolvemos 1
    if pd.isna(dorms) and 'estudio' in texto:
        return 1.0
        
    return dorms

# Aplicamos las funciones
print("Extrayendo m2...")
df['m2_totales'] = df['Detalles'].apply(lambda x: extraer_numeros(x, 'm²'))

print("Extrayendo dormitorios...")
df['dormitorios'] = df['Detalles'].apply(limpiar_dorms)

print("Extrayendo baños...")
df['banos'] = df['Detalles'].apply(lambda x: extraer_numeros(x, 'baño'))

# --- LIMPIEZA UBICACIÓN ---
def extraer_comuna(texto):
    if pd.isna(texto): return "Desconocida"
    parts = str(texto).split(',')
    # La comuna suele ser el último o penúltimo elemento
    # Ej: "Calle X, Barrio Y, Santiago" -> Santiago
    # Ej: "Calle X, Providencia, Santiago" -> Providencia? A veces es confuso.
    # Estrategia simple: Tomar el penúltimo si existe, si no el último.
    # Ajusta esto según tus datos. En Portalinmobiliario: "Dirección, Barrio, Comuna"
    if len(parts) >= 3:
        return parts[-1].strip() # Último elemento
    elif len(parts) == 2:
        return parts[-1].strip()
    return parts[0].strip()

print("Extrayendo comunas...")
df['comuna'] = df['Ubicacion'].apply(extraer_comuna)

# --- CREACIÓN DE MÉTRICA DE VALOR ---
# Esta es la variable MÁS IMPORTANTE para un inversionista
df['precio_m2'] = df['precio_peso'] / df['m2_totales']

# Filtrar basura (Filas sin precio o sin m2)
df_clean = df.dropna(subset=['precio_peso', 'm2_totales'])

# --- REPORTE FINAL ---
print("\n=== REPORTE DE INGENIERÍA DE DATOS ===")
print(df_clean[['Ubicacion', 'comuna', 'precio_peso', 'm2_totales', 'dormitorios']].head())
print("\nEstadísticas de Precio/m2:")
print(df_clean['precio_m2'].describe().apply(lambda x: format(x, 'f')))

# Guardar
df_clean.to_csv("datos_inmobiliarios_procesados.csv", index=False)
print("\n¡Archivo final guardado: 'datos_inmobiliarios_procesados.csv'!")
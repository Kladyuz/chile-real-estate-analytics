import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="InmoAnalytics Chile", layout="wide")

st.title("🇨🇱 Análisis de Mercado Inmobiliario - Santiago")
st.markdown("""
Esta herramienta permite a inversionistas identificar oportunidades inmobiliarias 
analizando el **Precio por m²** y tendencias de mercado.
""")

# 2. CARGA DE DATOS
# Usamos caché para que no recargue el CSV cada vez que tocas un botón (Eficiencia)
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\javie\Desktop\Javier Ingeniero\Portfolio_Projects\proyecto_inmobiliario\FASE 3\datos_inmobiliarios_procesados.csv")
    return df

df = load_data()

# 3. SIDEBAR (FILTROS)
st.sidebar.header("Filtros")

# Filtro de Dormitorios
dorms_filter = st.sidebar.multiselect(
    "Cantidad de Dormitorios",
    options=sorted(df['dormitorios'].dropna().unique()),
    default=sorted(df['dormitorios'].dropna().unique())
)

# Filtro de Precio
price_range = st.sidebar.slider(
    "Rango de Precio (CLP)",
    min_value=int(df['precio_peso'].min()),
    max_value=int(df['precio_peso'].max()),
    value=(int(df['precio_peso'].min()), int(df['precio_peso'].max()))
)

# APLICAR FILTROS
df_filtered = df[
    (df['dormitorios'].isin(dorms_filter)) &
    (df['precio_peso'].between(price_range[0], price_range[1]))
]

# 4. KPIs (Métricas Clave)
col1, col2, col3 = st.columns(3)
col1.metric("Propiedades Analizadas", f"{len(df_filtered)}")
col2.metric("Precio Promedio", f"${df_filtered['precio_peso'].mean():,.0f}")
col3.metric("Precio/m² Promedio", f"${df_filtered['precio_m2'].mean():,.0f}")

# 5. GRÁFICOS

# Fila 1
c1, c2 = st.columns(2)

with c1:
    st.subheader("Distribución de Precios")
    fig_hist = px.histogram(df_filtered, x="precio_peso", nbins=20, title="Histograma de Precios", color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.subheader("Relación Tamaño vs Precio")
    # Este gráfico es clave para ver oportunidades (los puntos abajo a la derecha son gangas: grandes y baratos)
    fig_scatter = px.scatter(
        df_filtered, 
        x="m2_totales", 
        y="precio_peso", 
        color="dormitorios",
        size="precio_m2",
        hover_data=['Ubicacion'],
        title="Precio vs m² (Color = Dorms)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Fila 2
st.subheader("Top 5 Propiedades más 'Baratas' (por m²)")
# Ordenamos por precio_m2 ascendente (las más baratas primero)
top_oportunidades = df_filtered.sort_values(by="precio_m2").head(5)
st.dataframe(top_oportunidades[['Ubicacion', 'precio_peso', 'm2_totales', 'precio_m2', 'Detalles']])

# 6. FOOTER
st.markdown("---")
st.caption("Desarrollado por Javier Molina para Portafolio de Data Science.")
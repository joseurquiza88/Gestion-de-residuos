import streamlit as st
import pandas as pd

import analysis as an
import plots as pl
import report as rp

st.set_page_config(layout="wide")


st.markdown("""
<div style="padding:20px; background: linear-gradient(90deg, #1b4332, #2d6a4f);
            border-radius:16px; color:white;">
    <h1>♻️ Economía Circular & Gestión de Residuos</h1>
    <h3>Indicadores clave para la toma de decisiones ambientales</h3>
</div>
""", unsafe_allow_html=True)

st.write("")
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)


# -------------------------
# CARGA
# -------------------------

df_gen = an.load_generados("data/residuos_generados.csv")
df_trat = an.load_tratados("data/residuos_tratados.csv")
factores = pd.read_csv("data/factores_co2.csv")

# -------------------------
# KPI
# -------------------------

total_gen = an.total_generado(df_gen)
total_trat = an.total_tratado(df_trat)
eficiencia = an.eficiencia_valorizacion(df_gen, df_trat)

df_co2 = an.calcular_co2(df_trat, factores)
co2_gen, co2_evit, co2_neto = an.resumen_co2(df_co2)

# -------------------------
# HERO
# -------------------------

st.markdown("""
# ♻️ Economía Circular & Gestión de Residuos  
### Indicadores clave para la toma de decisiones ambientales
""")

st.markdown(
    """
    <style>
    /* Fondo general */
    .stApp {
        background-color: #f4f7f6;
        font-family: "Inter", sans-serif;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #1b4332;
        font-weight: 600;
    }

    /* Subtítulos */
    h4, h5, h6 {
        color: #2d6a4f;
    }

    /* Tarjetas KPI */
    div[data-testid="metric-container"] {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.04);
    }

    /* Alerts */
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------
# KPIs
# -------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Residuos generados", f"{total_gen/1000:.1f} t")
col2.metric("Residuos valorizados", f"{total_trat/1000:.1f} t")
col3.metric("Eficiencia", f"{eficiencia:.1f} %")
col4.metric("CO₂ evitado", f"{co2_evit/1000:.1f} t")

# -------------------------
# METAS
# -------------------------
st.subheader("🚦 Cumplimiento de metas ambientales")

META_EF = 70
META_CO2 = 10_000

c1, c2 = st.columns(2)

with c1:
    if eficiencia >= META_EF:
        st.success("🟢 Meta de eficiencia cumplida")
    else:
        st.warning("🟡 Eficiencia bajo objetivo")

with c2:
    if co2_evit >= META_CO2:
        st.success("🟢 Meta de CO₂ cumplida")
    else:
        st.warning("🟡 CO₂ evitado insuficiente")




# -------------------------
# SANKEY
# -------------------------

st.subheader("🔁 Flujo de residuos")
st.plotly_chart(pl.plot_sankey_residuos(df_trat, factores), use_container_width=True)

# -------------------------
# SERIES TEMPORALES
# -------------------------

st.subheader("📈 Evolución mensual")

df_ts = an.generacion_mensual(df_gen)
st.plotly_chart(pl.plot_generacion_mensual(df_ts), use_container_width=True)

# -------------------------
# DESTINOS
# -------------------------

st.subheader("♻️ Tratamiento por destino")
st.plotly_chart(pl.plot_tratados_por_destino(df_trat), use_container_width=True)

# -------------------------
# ALERTAS
# -------------------------

st.subheader("🚨 Alertas")
alertas = an.generar_alertas(df_gen, eficiencia)

if alertas:
    for icon, msg in alertas:
        st.warning(f"{icon} {msg}")
else:
    st.success("🟢 Operación dentro de parámetros óptimos")

# -------------------------
# RESUMEN
# -------------------------

st.subheader("📝 Resumen ejecutivo")
st.markdown(rp.resumen_ejecutivo(
    total_gen, total_trat, eficiencia, co2_evit, co2_neto
))

import pandas as pd

# -------------------------
# CARGA DE DATOS
# -------------------------

def load_generados(path):
    df = pd.read_csv(path, encoding="latin-1")
    df["mes"] = pd.to_datetime(df["mes"])
    return df

def load_tratados(path):
    df = pd.read_csv(path, encoding="latin-1")
    df["mes"] = pd.to_datetime(df["mes"])
    return df


# -------------------------
# INDICADORES
# -------------------------

def total_generado(df_gen):
    return df_gen["kg_generados"].sum()

def total_tratado(df_trat):
    return df_trat["kg_tratados"].sum()

def eficiencia_valorizacion(df_gen, df_trat):
    gen = total_generado(df_gen)
    trat = total_tratado(df_trat)
    return (trat / gen) * 100 if gen > 0 else 0


# -------------------------
# SERIES TEMPORALES
# -------------------------

def generacion_mensual(df_gen):
    return (
        df_gen.groupby(["mes", "residuo_generado"])["kg_generados"]
        .sum()
        .reset_index()
    )


# -------------------------
# CO2
# -------------------------

def calcular_co2(df_trat, factores):
    df = df_trat.merge(factores, on="destino", how="left")
    df["co2"] = df["kg_tratados"] * df["factor_co2"]
    return df

def resumen_co2(df):
    generado = df[df["factor_co2"] > 0]["co2"].sum()
    evitado = abs(df[df["factor_co2"] < 0]["co2"].sum())
    neto = evitado - generado
    return generado, evitado, neto


# -------------------------
# ALERTAS
# -------------------------

def generar_alertas(df_gen, eficiencia):
    alertas = []

    if eficiencia < 50:
        alertas.append(("⚠️", "Eficiencia de valorización menor al 50%"))

    peligrosos = df_gen[df_gen["residuo_generado"] == "Peligrosos"]["kg_generados"].sum()
    if peligrosos > 500:
        alertas.append(("☣️", "Alto volumen de residuos peligrosos"))

    return alertas

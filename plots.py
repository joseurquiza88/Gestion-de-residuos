import plotly.express as px
import plotly.graph_objects as go

# -------------------------
# SERIE TEMPORAL (FILTRABLE)
# -------------------------

def plot_generacion_mensual(df_ts):
    fig = px.line(
        df_ts,
        x="mes",
        y="kg_generados",
        color="residuo_generado",
        markers=True,
        title="Evolución mensual de residuos generados"
    )
    fig.update_layout(
        hovermode="x unified",
        legend_title="Residuo (click para ocultar)"
    )
    return fig


# -------------------------
# DESTINO DE RESIDUOS
# -------------------------

def plot_tratados_por_destino(df_trat):
    df = (
        df_trat.groupby("destino")["kg_tratados"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        df,
        x="destino",
        y="kg_tratados",
        title="Residuos tratados por destino",
        text_auto=".2s"
    )
    return fig


# -------------------------
# SANKEY
# -------------------------

def plot_sankey_residuos(df_trat, factores):
    df = df_trat.merge(factores, on="destino", how="left")

    fuentes = df["residuo_generado"].unique().tolist()
    destinos = df["destino"].unique().tolist()

    labels = fuentes + destinos
    source_map = {k: i for i, k in enumerate(fuentes)}
    target_map = {k: i + len(fuentes) for i, k in enumerate(destinos)}

    sources = df["residuo_generado"].map(source_map)
    targets = df["destino"].map(target_map)
    values = df["kg_tratados"]

    fig = go.Figure(go.Sankey(
        node=dict(label=labels, pad=15, thickness=20),
        link=dict(source=sources, target=targets, value=values)
    ))

    fig.update_layout(title="Flujo de residuos: Generado → Destino")
    return fig
